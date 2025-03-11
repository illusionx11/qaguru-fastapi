import pytest
import requests
from http import HTTPStatus
from models.User import User

@pytest.mark.users_tests
@pytest.mark.usefixtures("app_url", "users")
class TestUsers:                
    def test_users(self, app_url: str):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
    
        users = response.json()["items"]
        for user in users:
            User.model_validate(user)
            
    def test_users_no_duplicates(self, users: list[User]):
        users_ids = [user["id"] for user in users]
        assert len(users_ids) == len(set(users_ids))

    @pytest.mark.parametrize("user_id", [1, 6, 11])
    def test_user(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        
        user = response.json()
        User.model_validate(user)

    @pytest.mark.parametrize("user_id", [14, 100])
    def test_user_non_existent_values(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        
    @pytest.mark.parametrize("user_id", ["a", None, [55], -1, 0])
    def test_user_invalid_values(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    


