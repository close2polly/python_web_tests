# Условие: Добавить в проект тесты API, написанные в ходе первого семинара.
# Доработать эти тесты в едином стиле с тестами UI, добавив логирование и обработку ошибок.
# Должен получиться единый тестовый проект.

# Формат сдачи: проект на Python с обязательным использованием Pytest

import yaml
import pytest
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logging
import requests
import random


with open("selenium.yaml") as f:
    config_selenium = yaml.safe_load(f)

with open("config.yaml") as f:
    config = yaml.safe_load(f)


@pytest.fixture(scope="session")
def browser():
    # ChromeDriverManager у меня не работает
    service = Service(config_selenium["driver"])
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://test-stand.gb.ru"

    def find_element(self, locator, time=10):
        try:
            element = WebDriverWait(self.driver, time).until(
                EC.presence_of_element_located(locator), message=f"NOT FOUND {locator}"
            )
        except:
            logging.error("Элемент не найден")
            element = None
        return element

    def get_element_property(self, locator, property):
        element = self.find_element(locator)
        if element:
            return element.value_of_css_property(property)
        else:
            logging.error(f"Свойство {property} не найдено с {locator}")
            return None

    def go_to_site(self):
        try:
            strart_browsing = self.driver.get(self.base_url)
        except:
            logging.error("Сайт не открылся")
            strart_browsing = None
        return strart_browsing

    def get_alert_text(self):
        try:
            alert = self.driver.switch_to.alert
            return alert.text
        except:
            logging.error("Alert не обнаружен")
            return None


class TestSearchLocators:
    ids = dict()
    with open("selectors.yaml") as f:
        locators = yaml.safe_load(f)
    for locator in locators["xpath"].keys():
        ids[locator] = (By.XPATH, locators["xpath"][locator])
    for locator in locators["css"].keys():
        ids[locator] = (By.CSS_SELECTOR, locators["css"][locator])


class OperationsHelper(BasePage):
    def enter_text_into_field(self, locator, word, description=None):
        if description:
            elem_name = description
        else:
            elem_name = locator
        logging.debug(f"Вставить {word} в {elem_name}")
        field = self.find_element(locator)
        if not field:
            logging.error(f"{locator} не найден")
            return False
        try:
            field.clear()
            field.send_keys(word)
        except:
            logging.error(f"Неудача с {locator}")
            return False
        return True

    def get_text_from_element(self, locator, description=None):
        if description:
            elem_name = description
        else:
            elem_name = locator
        logging.debug(f"Получить текст из {elem_name}")
        field = self.find_element(locator)
        if not field:
            return None
        try:
            text = field.text
        except:
            logging.error(f"Не получилось достать текст из {elem_name}")
            return None
        logging.debug(f"Текст из {elem_name}: {text}")
        return text

    def click_button(self, locator, description=None):
        if description:
            elem_name = description
        else:
            elem_name = locator
        logging.debug(f"Хотим нажать на {elem_name}")
        button = self.find_element(locator)
        if not button:
            return False
        try:
            button.click()
        except:
            logging.error(f"Не получилось нажать на {elem_name}")
            return False
        logging.debug(f"Нажади на {elem_name}")
        return True

    def enter_login(self, word):
        self.enter_text_into_field(
            TestSearchLocators.ids["LOCATOR_LOGIN_FIELD"], word, description="Логин"
        )

    def enter_pass(self, word):
        self.enter_text_into_field(
            TestSearchLocators.ids["LOCATOR_PASS_FIELD"], word, description="Пароль"
        )

    def click_login_button(self):
        self.click_button(
            TestSearchLocators.ids["LOCATOR_LOGIN_BTN"], description="Войти"
        )

    def get_error_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_ERROR_FIELD"])

    def get_user_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_HELLO"])

    def click_new_post_btn(self):
        self.click_button(
            TestSearchLocators.ids["LOCATOR_NEW_POST_BTN"], description="Создать пост"
        )

    def enter_title(self, word):
        self.enter_text_into_field(
            TestSearchLocators.ids["LOCATOR_TITLE"], word, description="Заголовок"
        )

    def enter_description(self, word):
        self.enter_text_into_field(
            TestSearchLocators.ids["LOCATOR_DESCRIPTION"], word, description="Описание"
        )

    def click_save_btn(self):
        self.click_button(
            TestSearchLocators.ids["LOCATOR_SAVE_BUTTON"], description="Сохранить"
        )

    def get_res_text(self):
        return self.get_text_from_element(TestSearchLocators.ids["LOCATOR_NEW_TITLE"])

    def click_contact_us(self):
        self.click_button(
            TestSearchLocators.ids["LOCATOR_CONTACT_US_BTN"], description="Связаться"
        )

    def enter_your_name(self, word):
        self.enter_text_into_field(
            TestSearchLocators.ids["LOCATOR_YOUR_NAME"], word, description="Имя"
        )

    def enter_email(self, word):
        self.enter_text_into_field(
            TestSearchLocators.ids["LOCATOR_EMAIL"], word, description="Почта"
        )

    def click_send_contact(self):
        self.click_button(
            TestSearchLocators.ids["LOCATOR_SEND_CONTACT_US"],
            description="Отправить контакты",
        )

    def get_alert(self):
        logging.info("Получает текст alert")
        text = self.get_alert_text()
        logging.info(f"Тест: {text}")
        return text


class ApiAuth:
    def __init__(self):
        self.auth_url = "https://test-stand.gb.ru/gateway/login"

    def get_token(self):
        logging.info("Получаем токен")
        try:
            res = requests.post(
                self.auth_url,
                data={"username": config["username"], "password": config["password"]},
            )
            answer = res.json()
            token = answer["token"]
        except:
            logging.error("Ошибка получения токена")
            token = None
        logging.debug(f"Токен: {token}")
        return token


class ApiMethods(ApiAuth):
    def __init__(self):
        super().__init__()
        self.posts_url = "https://test-stand.gb.ru/api/posts"

    def get_posts(self):
        logging.info(f"Получаем все посты")
        headers = {"X-Auth-Token": self.get_token()}
        try:
            res = requests.get(self.posts_url, params={"page": 1}, headers=headers)
            answer = res.json()
            descriptions = [i["description"] for i in answer["data"]]
        except: 
            logging.error(f"Ошибка получения постов")
            descriptions = []
        logging.debug(f"Посты: {descriptions}")
        return descriptions

    def create_post(self):
        headers = {"X-Auth-Token": self.get_token()}
        logging.info(f"создаем новый пост")
        try:
            res = requests.post(
                self.posts_url,
                data={
                    "title": "Тест",
                    "description": "Тест " + str(random.randint(0, 100)),
                    "content": "Тест",
                },
                headers=headers,
            )
            answer = res.json()
        except:
            logging.error(f"Ошибка получения постов")
            answer = None
        logging.debug(f"Пост: {answer}")
        return answer


def test_1(browser):
    testpage = OperationsHelper(browser)
    testpage.go_to_site()
    testpage.enter_login("test")
    testpage.enter_pass("test")
    testpage.click_login_button()
    assert testpage.get_error_text() == "401"


def test_2(browser):
    testpage = OperationsHelper(browser)
    testpage.enter_login(config["username"])
    testpage.enter_pass(config["password"])
    testpage.click_login_button()
    assert testpage.get_user_text() == f"Hello, {config["username"]}"


def test_3(browser):
    testpage = OperationsHelper(browser)
    testpage.click_new_post_btn()
    testpage.enter_title("testtest")
    testpage.enter_description("testtest")
    testpage.click_save_btn()
    time.sleep(10)
    assert testpage.get_res_text() == "testtest"


def test_4(browser):
    testpage = OperationsHelper(browser)
    testpage.click_contact_us()
    testpage.enter_your_name("Test Testov")
    testpage.enter_email("test@test.ru")
    testpage.click_send_contact()
    time.sleep(10)
    assert testpage.get_alert() == "Form successfully submitted"

def test_5():
    testapi = ApiMethods()
    last_post = testapi.create_post()
    all_posts = testapi.get_posts()
    assert last_post["description"] in all_posts

