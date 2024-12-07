# Условие: Добавить в проект тест по проверке механики работы формы Contact Us
# на главной странице личного кабинета.
# Должно проверятся открытие формы, ввод данных в поля, клик по кнопке и появление всплывающего alert.

# Совет: переключиться на alert можно командой alert = self.driver.switch_to.alert
# Вывести текст alert.text

# Формат сдачи: В качестве решения принимается
# написанный нами ранее проект с добавлением шага по проверке Contact Us
# и правками всех необходимых вспомогательных файлов.

import yaml
import pytest
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

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
        return WebDriverWait(self.driver, time).until(
            EC.presence_of_element_located(locator), message=f"NOT FOUND {locator}"
        )

    def get_element_property(self, locator, property):
        element = self.find_element(locator)
        return element.value_of_css_property(property)

    def go_to_site(self):
        return self.driver.get(self.base_url)


class TestSearchLocators:
    LOCATOR_LOGIN_FIELD = (By.XPATH, """//*[@id="login"]/div[1]/label/input""")
    LOCATOR_PASS_FIELD = (By.XPATH, """//*[@id="login"]/div[2]/label/input""")
    LOCATOR_LOGIN_BTN = (By.CSS_SELECTOR, """button""")
    LOCATOR_ERROR_FIELD = (By.XPATH, """//*[@id="app"]/main/div/div/div[2]/h2""")
    LOCATOR_HELLO = (By.XPATH, """//*[@id="app"]/main/nav/ul/li[3]/a""")
    LOCATOR_NEW_POST_BTN = (
        By.XPATH,
        """//*[@id="create-btn"]""",
    )
    LOCATOR_TITLE = (
        By.XPATH,
        """//*[@id="app"]/main/div/div/form/div/div/div[1]/div/label/input""",
    )
    LOCATOR_DESCRIPTION = (
        By.XPATH,
        """//*[@id="app"]/main/div/div/form/div/div/div[2]/div/label/span/textarea""",
    )
    LOCATOR_SAVE_BUTTON = (
        By.XPATH,
        """//*[@id="app"]/main/div/div/form/div/div/div[7]/div/button""",
    )
    LOCATOR_NEW_TITLE = (
        By.XPATH,
        """//*[@id="app"]/main/div/div[1]/h1""",
    )
    LOCATOR_CONTACT_US_BTN = (By.XPATH, """//*[@id="app"]/main/nav/ul/li[2]/a""")
    LOCATOR_YOUR_NAME = (By.XPATH, """//*[@id="contact"]/div[1]/label/input""")
    LOCATOR_EMAIL = (By.XPATH, """//*[@id="contact"]/div[2]/label/input""")
    LOCATOR_SEND_CONTACT_US = (By.XPATH, """//*[@id="contact"]/div[4]/button""")


class OperationsHelper(BasePage):
    def enter_login(self, word):
        login_field = self.find_element(TestSearchLocators.LOCATOR_LOGIN_FIELD)
        login_field.clear()
        login_field.send_keys(word)

    def enter_pass(self, word):
        pass_field = self.find_element(TestSearchLocators.LOCATOR_PASS_FIELD)
        pass_field.clear()
        pass_field.send_keys(word)

    def click_login_button(self):
        self.find_element(TestSearchLocators.LOCATOR_LOGIN_BTN).click()

    def get_error_text(self):
        error_field = self.find_element(TestSearchLocators.LOCATOR_ERROR_FIELD)
        return error_field.text

    def get_user_text(self):
        user_field = self.find_element(TestSearchLocators.LOCATOR_HELLO)
        return user_field.text

    def click_new_post_btn(self):
        self.find_element(TestSearchLocators.LOCATOR_NEW_POST_BTN).click()

    def enter_title(self, word):
        title_field = self.find_element(TestSearchLocators.LOCATOR_TITLE)
        title_field.clear()
        title_field.send_keys(word)

    def enter_description(self, word):
        description_field = self.find_element(TestSearchLocators.LOCATOR_DESCRIPTION)
        description_field.clear()
        description_field.send_keys(word)

    def click_save_btn(self):
        self.find_element(TestSearchLocators.LOCATOR_SAVE_BUTTON).click()

    def get_res_text(self):
        new_title = self.find_element(TestSearchLocators.LOCATOR_NEW_TITLE)
        return new_title.text

    def click_contact_us(self):
        self.find_element(TestSearchLocators.LOCATOR_CONTACT_US_BTN).click()

    def enter_your_name(self, word):
        your_name_field = self.find_element(TestSearchLocators.LOCATOR_YOUR_NAME)
        your_name_field.send_keys(word)

    def enter_email(self, word):
        email_field = self.find_element(TestSearchLocators.LOCATOR_EMAIL)
        email_field.send_keys(word)

    def click_send_contact(self):
        self.find_element(TestSearchLocators.LOCATOR_SEND_CONTACT_US).click()

    def show_aler(self):
        alert = self.driver.switch_to.alert
        return alert.text


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
    assert testpage.show_aler() == "Form successfully submitted"
