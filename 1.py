# Условие: Добавить в задание с REST API ещё один тест,
# в котором создаётся новый пост,
# а потом проверяется его наличие на сервере по полю «описание».
# Подсказка: создание поста выполняется запросом к https://test-stand.gb.ru/api/posts с передачей параметров title, description, content.

import yaml
import pytest
import requests
import random

with open("config.yaml") as f:
    config = yaml.safe_load(f)


@pytest.fixture()
def login():
    res = requests.post(
        config["auth_url"],
        data={"username": config["username"], "password": config["password"]},
    )
    answer = res.json()
    return answer["token"]


@pytest.fixture()
def get_posts(login):
    headers = {"X-Auth-Token": login}
    res = requests.get(config["posts_url"], params={ "page": 1 }, headers=headers)
    answer = res.json()
    descriptions = [i["description"] for i in answer["data"]]
    return descriptions

@pytest.fixture()
def create_post(login):
    headers = {"X-Auth-Token": login}
    res = requests.post(
        config["posts_url"],
        data={"title": "Тест", "description": "Тест " + str(random.randint(0, 100)), "content": "Тест"},
        headers=headers,
    )
    answer = res.json()
    return answer


def test(create_post, get_posts):
    assert create_post["description"] in get_posts
