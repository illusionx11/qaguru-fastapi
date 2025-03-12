import pytest
import dotenv
import os
import requests
from http import HTTPStatus

@pytest.fixture(autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture
def app_url() -> str:
    return os.getenv("APP_URL")

@pytest.fixture
def users(app_url: str):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]
