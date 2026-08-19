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
│    └── test_posts.py     # Тесты для эндпоинта /posts
├── README.md
├── requirements.txt
└── .gitignore
```

## Требования

- Python 3.12
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

### Запуск всех тестов

```bash
pytest
```

### Запуск с подробным выводом

```bash
pytest -v
```

### Запуск только тестов из класса `TestPosts`

```bash
pytest tests/test_posts.py::TestPosts -v
```

### Запуск конкретного теста по имени

```bash
pytest tests/test_posts.py::TestPosts::test_get_all_posts -v
```

### Запуск с отображением print-вывода

```bash
pytest -v -s
```

### Запуск только негативных тестов (по маркеру в имени)

```bash
pytest -v -k "nonexistent or invalid"
```

## Ожидаемый результат