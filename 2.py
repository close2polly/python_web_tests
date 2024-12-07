# Условие: Добавить в наш тестовый проект шаг добавления поста после входа.
# Должна выполняться проверка на наличие названия поста на странице сразу после его создания.
# Совет: не забудьте добавить небольшие ожидания перед и после нажатия кнопки создания поста.

import yaml
import pytest
from module import Site
from selenium.webdriver.common.by import By
import time

with open("config.yaml") as f:
    config = yaml.safe_load(f)


@pytest.fixture()
def x_username_selector():
    return """//*[@id="login"]/div[1]/label/input"""


@pytest.fixture()
def x_password_selector():
    return """//*[@id="login"]/div[2]/label/input"""


@pytest.fixture()
def css_btn_selector():
    return """button"""


@pytest.fixture()
def x_greeting_selector():
    return """//*[@id="app"]/main/nav/ul/li[3]/a"""


@pytest.fixture()
def expected():
    return "Hello, {}".format(config["username"])


@pytest.fixture()
def x_title_post():
    return """//*[@id="app"]/main/div/div/form/div/div/div[1]/div/label/input"""


@pytest.fixture()
def x_button_post():
    return """//*[@id="app"]/main/div/div/form/div/div/div[7]/div/button"""


@pytest.fixture()
def x_new_post_title():
    return """//*[@id="app"]/main/div/div[1]/h1"""


site = Site(config["login_url"])


def test(
    x_username_selector,
    x_password_selector,
    css_btn_selector,
    x_greeting_selector,
    expected,
    x_title_post,
    x_button_post,
    x_new_post_title,
):
    input_username = site.find_element("xpath", x_username_selector)
    input_username.send_keys(config["username"])

    input_username = site.find_element("xpath", x_password_selector)
    input_username.send_keys(config["password"])

    btn = site.find_element("css", css_btn_selector)
    btn.click()

    # Протухает сессия
    user_label = site.wait_element(x_greeting_selector)

    create_btn = site.driver.find_element(By.ID, "create-btn")
    create_btn.click()

    input_title_create = site.find_element("xpath", x_title_post)
    input_title_create.send_keys("Тест Тест Тест")

    save_btn = site.find_element("xpath", x_button_post)
    save_btn.click()

    time.sleep(30)

    new_post_title = site.wait_element(x_new_post_title)
    print(new_post_title.text)

    assert new_post_title.text == "Тест Тест Тест"

