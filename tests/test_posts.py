import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"
POSTS_ENDPOINT = f"{BASE_URL}/posts"

# Ожидаемый набор ключей
EXPECTED_POST_KEYS = {"userId", "id", "title", "body"}


class TestPosts:
    """Класс с тестами для работы с ресурсом /posts."""

    # GET

    def test_get_all_posts(self, session):
        """GET /posts возвращает список всех постов со статусом 200."""
        response = session.get(POSTS_ENDPOINT)

        assert response.status_code == 200, (
            f"Ожидался статус 200, получен {response.status_code}"
        )

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
        """GET /posts/<id> возвращает пост по ID или 404, если его нет."""
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