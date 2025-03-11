import pytest
import requests
from http import HTTPStatus

@pytest.mark.pagination
@pytest.mark.usefixtures("app_url")
class TestPagination:
    
    def test_users_pagination_total(self, app_url: str):
        """
        Тест на проверку общего количества записей (пользователей) в пагинации
        """
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
    
        total = response.json()["total"]
        assert total == 12

    @pytest.mark.parametrize(
        "pagination_data", [
            {"page": 1, "expected_users": 10},
            {"page": 2, "expected_users": 2}
        ]
    )
    def test_users_pagination_expected_users(self, app_url: str, pagination_data: list[dict]):
        """
        Тест на проверку определенного количества записей (пользователей) в пагинации при фиксированном значении size
        """
        page = pagination_data["page"]
        response = requests.get(f"{app_url}/api/users/", params={"page": page, "size": 10})
        assert response.status_code == HTTPStatus.OK
        
        users = response.json()["items"]
        assert len(users) == pagination_data["expected_users"]

    @pytest.mark.parametrize(
        "data", 
        [
            {"page": 1, "first_user_id": 1, "last_user_id": 10},
            {"page": 2, "first_user_id": 11, "last_user_id": 12}
        ]
    )
    def test_users_pagination_page_info_correct(self, app_url: str, data: dict):
        """
        Тест на проверку корректных записей (пользователей) на разных страницах
        """
        page = data["page"]
        response = requests.get(f"{app_url}/api/users/", params={"page": page, "size": 10})
        assert response.status_code == HTTPStatus.OK
        
        users = response.json()["items"]
        assert users[0]["id"] == data["first_user_id"]
        assert users[-1]["id"] == data["last_user_id"]

    @pytest.mark.parametrize(
        "pagination_data", 
        [
            {"size": 5, "expected_pages": 3},
            {"size": 3, "expected_pages": 4},
            {"size": 1, "expected_pages": 12}
        ]
    )
    def test_users_pagination_expected_pages(self, app_url: str, pagination_data: list[dict]):
        """
        Тест на проверку количества страниц в пагинации при фиксированном значении size
        """
        size = pagination_data["size"]
        response = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": size})
        assert response.status_code == HTTPStatus.OK

        pages = response.json()["pages"]
        assert pages == pagination_data["expected_pages"]
        
    def test_users_pagination_wrong_page(self, app_url: str):
        """
        Тест на проверку количества записей (пользователей) на несуществующей странице
        """
        response = requests.get(f"{app_url}/api/users/", params={"page": 100, "size": 10})
        assert response.status_code == HTTPStatus.OK
        users = response.json()["items"]
        assert len(users) == 0

