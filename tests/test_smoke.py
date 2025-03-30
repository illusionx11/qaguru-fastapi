import pytest
import requests
import random
from http import HTTPStatus
from app.models.User import User
from app.models.AppStatus import AppStatus
from tests.utils.api import APIWrapper


@pytest.mark.smoke
@pytest.mark.usefixtures("users", "api_wrapper")
class TestSmoke:
    
    @pytest.fixture(autouse=True)
    def setup(self, api_wrapper: APIWrapper):
        self.api_wrapper = api_wrapper
    
    def test_smoke_status(self):
        response = self.api_wrapper.get_status()
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        AppStatus.model_validate(result)
        assert result["database"] == True

    def test_smoke_users(self):
        response = self.api_wrapper.get_users()
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        assert "items" in result
        assert isinstance(result["items"], list)

    def test_smoke_user(self, users: list[User]):
        user_id = random.choice(users)["id"]
        response = self.api_wrapper.get_user(user_id)
        assert response.status_code == HTTPStatus.OK






