"""Общие фикстуры и настройки для тестов"""

import pytest
import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="function")
def session():
    """
    Фикстура, которая создаёт экземпляр requests.Session для каждого теста.
    После завершения теста сессия закрывается.

    Scope='function' обеспечивает идемпотентность и независимость тестов друг от друга.
    """
    test_session = requests.Session()
    test_session.headers.update({
        "Content-Type": "application/json; charset=UTF-8",
        "Accept": "application/json",
    })
    yield test_session
    test_session.close()