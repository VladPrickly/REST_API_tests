# Автоматизированные тесты REST API JSONPlaceholder

Набор автоматизированных тестов на Python с использованием библиотеки `pytest`
для проверки базовых HTTP-операций (GET, POST, PUT, DELETE) эндпоинта
`/posts` публичного API [JSONPlaceholder](https://jsonplaceholder.typicode.com).

## Возможности

- Проверка всех базовых HTTP-методов: **GET, POST, PUT, DELETE**
- Валидация статус-кодов ответов
- Проверка структуры JSON-ответа 
- Проверка содержимого данных
- Параметризация тестов (`@pytest.mark.parametrize`) для множественных сценариев
- Негативные тесты (несуществующие ресурсы, некорректные данные)
- Идемпотентные тесты, не зависящие от порядка выполнения
- Использование `requests.Session` через фикстуру `pytest`

## Структура проекта

```
project
│
├── tests/
│    ├── conftest.py       # Фикстуры и настройки для тестов
│    └── test_posts.py     # Тесты для эндпоинтов GET, POST, PUT, DELETE
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Требования

- Python 3.8+
- Доступ в интернет 


## Локальная установка 
1. Создайте виртуальное окружение:
- Windows:
  ```
  python -m venv .venv
  ```
- Linux/macOS:
  ```
  python3 -m venv .venv
  ```

2. Активируйте виртуальное окружение:
- Windows:
  ```
  .venv\Scripts\activate
  ```
- Linux/macOS:
  ```
  source .venv/bin/activate
  ```
  
3. Установите зависимости
  ```
  pip install -r requirements.txt
  ```

##  Запуск тестов
  ```
  pytest                          # Все тесты
  pytest -v                       # Подробный вывод
  pytest -k "nonexistent"         # Только негативные тесты
  ```

## Ожидаемый результат (Пример)
  ```
============================= test session starts ==============================
platform linux -- Python 3.11.16, pytest-9.1.1, pluggy-1.6.0 -- /usr/local/bin/python3.11
cachedir: .pytest_cache
rootdir: /project
collecting ... collected 14 items

tests/test_posts.py::TestPosts::test_get_all_posts PASSED                [  7%]
tests/test_posts.py::TestPosts::test_get_post_by_id[existing_post_5] PASSED [ 21%]
tests/test_posts.py::TestPosts::test_get_post_by_id[existing_post_100] PASSED [ 28%]
tests/test_posts.py::TestPosts::test_get_post_by_id[nonexistent_post] PASSED [ 35%]
tests/test_posts.py::TestPosts::test_create_post[simple_post] PASSED     [ 42%]
tests/test_posts.py::TestPosts::test_create_post[unicode_post] PASSED    [ 50%]
tests/test_posts.py::TestPosts::test_create_post[long_content] PASSED    [ 57%]
tests/test_posts.py::TestPosts::test_update_post[update_existing_1] PASSED [ 64%]
tests/test_posts.py::TestPosts::test_update_post[update_existing_5] PASSED [ 71%]
tests/test_posts.py::TestPosts::test_update_post[update_nonexistent] PASSED [ 78%]
tests/test_posts.py::TestPosts::test_delete_post PASSED                  [ 85%]
tests/test_posts.py::TestPosts::test_get_nonexistent_post_returns_404 PASSED [ 92%]
tests/test_posts.py::TestPosts::test_post_with_invalid_payload PASSED    [100%]

============================== 14 passed in 5.45s ==============================
  ```


## Установка Через Docker (рекомендуется)

### 1. Сборка образа

  ```
  docker build -t rest-api-tests .
  ```

### 2. Запуск всех тестов

  ```
  docker run --rm rest-api-tests  
  ```


## Автор
- Владислав
- telegram: @vlad_705
- [e-mail](vlad.prickly@gmail.com)
- [github.com](https://github.com/VladPrickly)