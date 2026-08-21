import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"
POSTS_ENDPOINT = f"{BASE_URL}/posts"

EXPECTED_POST_KEYS = {"userId", "id", "title", "body"}


class TestPosts:
    """
    Класс с тестами для работы с ресурсом JSONPlaceholder.
    """

    # GET

    def test_get_all_posts(self, session):
        """
        GET запрос возвращает список всех постов со статусом 200.
        """
        response = session.get(POSTS_ENDPOINT)

        assert response.status_code == 200, (f"Ожидался статус 200, получен {response.status_code}")

        data = response.json()
        assert isinstance(data, list), "Ответ должен быть списком"
        assert len(data) > 0, "Список постов не должен быть пустым"

        # Проверяем структуру первого элемента списка
        first_post = data[0]
        assert EXPECTED_POST_KEYS.issubset(set(first_post.keys())), (
            "В объекте поста отсутствуют ожидаемые ключи"
        )

    @pytest.mark.parametrize(
        "post_id, expected_status",
        [
            pytest.param(1, 200, id="existing_post_1"),
            pytest.param(5, 200, id="existing_post_5"),
            pytest.param(100, 200, id="existing_post_100"),
            pytest.param(99999, 404, id="nonexistent_post"),  # негативный
        ],
    )

    def test_get_post_by_id(self, session, post_id, expected_status):
        """
        GET запрос возвращает ответ по запрашиваемому ID или 404, если такого ID нет.
        """
        response = session.get(f"{POSTS_ENDPOINT}/{post_id}")

        assert response.status_code == expected_status, (
            f"Для id={post_id} ожидался статус {expected_status}, "
            f"получен {response.status_code}"
        )

        if expected_status == 200:
            data = response.json()
            assert data["id"] == post_id, "ID в ответе не совпадает с запрошенным"
            assert EXPECTED_POST_KEYS == set(data.keys()), (
                "Структура ответа не соответствует ожидаемой"
            )
            assert isinstance(data["title"], str) and len(data["title"]) > 0
            assert isinstance(data["body"], str) and len(data["body"]) > 0


    # POST

    @pytest.mark.parametrize(
        "payload",
        [
            pytest.param(
                    {"title": "test_title_1", "body": "test_body", "userId": 1},
                id="simple_post",
            ),
            pytest.param(
                {"title": "Тестовый_заголовок_2", "body": "Тестовое_тело_2", "userId": 2},
                id="unicode_post",
            ),
            pytest.param(
                {"title": "a" * 100, "body": "b" * 500, "userId": 10},
                id="long_content",
            ),
        ],
    )
    def test_create_post(self, session, payload):
        """
        Функция создаёт новый пост запрос и возвращает ответ 201.
        """
        response = session.post(POSTS_ENDPOINT, json=payload)

        assert response.status_code == 201, (
            f"Ожидался статус 201, получен {response.status_code}"
        )

        data = response.json()
        # Проверка структуры
        assert EXPECTED_POST_KEYS.issubset(set(data.keys())), (
            "В ответе отсутствуют ожидаемые ключи"
        )

        assert data["title"] == payload["title"]
        assert data["body"] == payload["body"]
        assert data["userId"] == payload["userId"]
        # JSONPlaceholder присваивает id=101 новому посту
        assert data["id"] == 101

    # PUT

    @pytest.mark.parametrize(
        "post_id, payload, expected_status",
        [
            pytest.param(
                1,
                {"title": "updated_title", "body": "updated_body", "userId": 1},
                200,
                id="update_existing_1",
            ),
            pytest.param(
                5,
                {"title": "another", "body": "content", "userId": 2},
                200,
                id="update_existing_5",
            ),
            pytest.param(
                99999,
                {"title": "x", "body": "y", "userId": 1},
                500, # JSONPlaceholder возвращает 500 вместо 404 для несуществующих ресурсов
                id="update_nonexistent",  # негативный
            ),
        ],
    )
    def test_update_post(self, session, post_id, payload, expected_status):
        """
        PUT запрос полностью заменяет данные по указанному ID или возвращает 404.
        """
        response = session.put(f"{POSTS_ENDPOINT}/{post_id}", json=payload)

        assert response.status_code == expected_status, (
            f"Для id={post_id} ожидался статус {expected_status}, "
            f"получен {response.status_code}"
        )

        if expected_status == 200:
            data = response.json()
            assert data["id"] == post_id, "ID в ответе не совпадает с запрошенным"
            assert data["title"] == payload["title"]
            assert data["body"] == payload["body"]
            assert data["userId"] == payload["userId"]
            assert EXPECTED_POST_KEYS == set(data.keys())

    # # DELETE


    def test_delete_post(self, session):
        """
        Запрос DELETE удаляет данные и возвращает 200.
        """
        response = session.delete(f"{POSTS_ENDPOINT}/1")

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )
        assert response.json() == {}, "Тело ответа при удалении должно быть пустым"


    # Негативный тест

    def test_get_nonexistent_post_returns_404(self, session):
        """ GET запрос несуществующего поста возвращает 404.
        Функция проверяет обработку сервером запросов к ресурсам, которых не существует.
        """
        nonexistent_id = 99999
        response = session.get(f"{POSTS_ENDPOINT}/{nonexistent_id}")

        assert response.status_code == 404, (
            f"Для несуществующего id={nonexistent_id} ожидался 404, "
            f"получен {response.status_code}"
        )

    def test_post_with_invalid_payload(self, session):
        """
        Функция проверяет поведение API при отправке некорректных данных (пустой запрос).
        """

        response = session.post(POSTS_ENDPOINT, json={})

        assert response.status_code == 201, (f"Ожидался статус 201, получен {response.status_code}")

        data = response.json()
        assert "id" in data
        assert data["id"] == 101

        assert "title" not in data, "Поле 'title' не должно добавляться автоматически"
        assert "body" not in data, "Поле 'body' не должно добавляться автоматически"
        assert "userId" not in data, "Поле 'userId' не должно добавляться автоматически"