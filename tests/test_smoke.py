import pytest
import requests
from http import HTTPStatus
from models.User import User
from models.AppStatus import AppStatus
import random

@pytest.mark.smoke
@pytest.mark.usefixtures("app_url", "users")
class TestSmoke:
    
    def test_smoke(self, app_url: str):
        response = requests.get(f"{app_url}/status/")
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        AppStatus.model_validate(result)
        assert result["users"] == True

    def test_smoke_users(self, app_url: str):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        assert "items" in result
        assert isinstance(result["items"], list)

    def test_smoke_user(self, app_url: str, users: list[User]):
        user_id = random.choice(users)["id"]
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK






