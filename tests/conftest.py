import pytest
import dotenv
import os
import requests
import json
from http import HTTPStatus
from faker import Faker

faker = Faker()

@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()

@pytest.fixture(scope="session")
def app_url() -> str:
    return os.getenv("APP_URL")

@pytest.fixture
def users(app_url: str):
    response = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": 100})
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]
    
@pytest.fixture(scope="session", autouse=True)
def fill_test_data(app_url: str):

    clear_generated_users(app_url)
    
    with open("users.json", "r", encoding="utf-8") as f:
        test_data_users = json.load(f)
    
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())
    
    user_ids = [user["id"] for user in api_users]
    
    yield user_ids

    clear_generated_users(app_url)
    
def clear_generated_users(app_url: str) -> None:

    response = requests.get(f"{app_url}/api/users/", params={"page": 1, "size": 100})
    users = response.json()["items"]
    
    generated_users = [user for user in users if "qaguru.autotest" in user["email"]]
    
    for user in generated_users:
        response = requests.delete(f"{app_url}/api/users/{user['id']}")
        
@pytest.fixture
def user_data() -> dict[str]:
    email = faker.email(domain="qaguru.autotest")
    first_name = faker.first_name()
    last_name = faker.last_name()
    avatar = f"https://reqres.in/img/faces/{first_name}-{last_name}.jpg"
    
    user_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "avatar": avatar
    }
    
    return user_data