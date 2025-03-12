import pytest
import requests
from http import HTTPStatus
from models.User import User

@pytest.mark.pagination
@pytest.mark.usefixtures("app_url", "users")
class TestPagination:
    
    def test_users_pagination_total(self, app_url: str, users: list[User]):
        """
        Тест на проверку общего количества записей (пользователей) в пагинации
        """
        
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
    
        total = response.json()["total"]
        assert total == len(users)

    @pytest.mark.parametrize("page", [1, 2])
    def test_users_pagination_expected_users(self, app_url: str, page: int, users: list[User]):
        """
        Тест на проверку ожидаемого количества объектов в ответе при фиксированном значении size
        """
        
        size = 10
        response = requests.get(f"{app_url}/api/users/", params={"page": page, "size": size})
        assert response.status_code == HTTPStatus.OK
        
        users_on_page = response.json()["items"]
        # Вычисление ожидаемого кол-ва пользователей для определенной страницы. 
        # max(0, ...) т.к. результат min может быть отрицательный (напр. когда страница 100, в ответе записей не будет, и min вернет отрицательное значение)
        expected_users_on_page = max(0, min(size, len(users) - (page - 1) * size))

        assert len(users_on_page) == expected_users_on_page

    @pytest.mark.parametrize("size", [5, 3, 1])
    def test_users_pagination_expected_pages(self, app_url: str, size: int, users: list[User]):
        """
        Тест на проверку того, что возвращается правильное количество страниц при разных значениях size
        """

        response = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": size})
        assert response.status_code == HTTPStatus.OK

        pages = response.json()["pages"]
        # Формула для расчета кол-ва страниц при заданном size
        # Если есть остаток, то добавление size - 1 гарантирует, что этот остаток будет учтен как дополнительная страница
        expected_pages = (len(users) + size - 1) // size
        assert pages == expected_pages
        
    def test_users_pagination_wrong_page(self, app_url: str, users: list[User]):
        """
        Тест на проверку количества записей (пользователей) на несуществующей странице
        """
        
        size = 10
        max_page = (len(users) + size - 1) // size
        
        response = requests.get(f"{app_url}/api/users/", params={"page": max_page + 1, "size": size})
        assert response.status_code == HTTPStatus.OK
        users = response.json()["items"]
        assert len(users) == 0

    def test_pagination_different_results_per_page(self, app_url: str):
        """
        Тест на проверку того, что возвращаются разные данные при разных значениях page
        """
        
        response_first = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": 5})
        response_second = requests.get(f"{app_url}/api/users/", params={"page": 2, "size": 5})
        
        res_first = response_first.json()
        res_second = response_second.json()
        
        assert res_first["page"] != res_second["page"]
        assert res_first["items"] != res_second["items"]
        