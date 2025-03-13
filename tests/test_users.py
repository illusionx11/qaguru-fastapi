import pytest
import requests
import random
from http import HTTPStatus
from app.models.User import User
from tests.utils.generate_user_data import generate_user_data


@pytest.mark.users_tests
@pytest.mark.usefixtures("app_url", "users", "fill_test_data")
class TestUsers:                
    
    def test_get_users(self, app_url: str):
        response = requests.get(f"{app_url}/api/users/")
        assert response.status_code == HTTPStatus.OK
        user_list = response.json()["items"]
        for user in user_list:
            User.model_validate(user)
    
    def test_get_users_no_duplicates(self, users: list[User]):
        users_ids = [user["id"] for user in users]
        assert len(users_ids) == len(set(users_ids))

    def test_get_single_user(self, app_url: str, fill_test_data: list[int]):
        for user_id in [fill_test_data[0], fill_test_data[-1]]:
            response = requests.get(f"{app_url}/api/users/{user_id}")
            assert response.status_code == HTTPStatus.OK
            
            user = response.json()
            User.model_validate(user)

    @pytest.mark.parametrize("user_id", [14, 100])
    def test_get_single_user_non_existent_values(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        
    @pytest.mark.parametrize("user_id", ["a", None, [55], -1, 0])
    def test_get_single_user_invalid_values(self, app_url: str, user_id: int):
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        
    def test_post_single_user(self, app_url: str):
        """
        Тест на post: создание. Предусловия: подготовленные тестовые данные
        Данные для отправки генерируются в generate_user_data() с помощью faker
        """
        user_data = generate_user_data()
        response = requests.post(f"{app_url}/api/users/", json=user_data)
        assert response.status_code == HTTPStatus.CREATED   
        user: dict = response.json()
        User.model_validate(user)
        del user['id']
        assert user_data == user
        
    def test_delete_single_user(self, app_url: str, users: list[User]):
        """ 
        Тест на delete: удаление. Предусловия: наличие созданного пользователя
        """

        user: dict = random.choice(users)
        response = requests.delete(f"{app_url}/api/users/{user['id']}")
        assert response.status_code == HTTPStatus.OK
        data: dict = response.json()
        assert data["message"] == "User deleted"
    
    @pytest.mark.parametrize("user_data", [
        {
            "email": "unique.mail.1@qaguru.autotest",
        },
        {
            "first_name": "UniqueFirstName1"
        },
        {
            "last_name": "UniqueLastName1"
        },
        {
            "avatar": "https://reqres.in/img/faces/unique-avatar-1.jpg"
        },
        {
            "email": "unique.mail.2@qaguru.autotest",
            "first_name": "UniqueFirstName2",
        },
        {
            "last_name": "UniqueLastName2",
            "avatar": "https://reqres.in/img/faces/unique-avatar-2.jpg"
        },
        {
            "first_name": "UniqueFirstName3",
            "last_name": "UniqueLastName3",
            "avatar": "https://reqres.in/img/faces/unique-avatar-3.jpg"
        },
        {
            "email": "unique.mail.4@qaguru.autotest",
            "first_name": "UniqueFirstName4",
            "last_name": "UniqueLastName4",
            "avatar": "https://reqres.in/img/faces/unique-avatar-4.jpg"
        }
    ])
    def test_patch_single_user(self, app_url: str, users: list[User], user_data: dict):
        """ 
        Тест на patch: изменение. Предусловия: наличие созданного пользователя
        Не использую faker т.к. значение в каком-нибудь из полей может повториться, тогда последний assert не пройдет
        """

        user: dict = random.choice(users)
        response = requests.patch(f"{app_url}/api/users/{user['id']}", json=user_data)
        assert response.status_code == HTTPStatus.OK
        updated_user: dict = response.json()
        User.model_validate(updated_user)
        assert user['id'] == updated_user['id']
        for key in user_data.keys():
            assert user[key] != updated_user[key]

    def test_get_user_after_post(self, app_url: str):
        """ 
        Тест на Get после создания
        """

        user_data = generate_user_data()
        response = requests.post(f"{app_url}/api/users/", json=user_data)
        assert response.status_code == HTTPStatus.CREATED   
        user: dict = response.json()
        user_id = user.pop("id", None)
        assert user == user_data
        
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        get_user: dict = response.json()
        get_user_id = get_user.pop("id", None)
        assert user_id == get_user_id
        assert get_user == user

    def test_get_user_after_patch(self, app_url: str, users: list[User]):
        """ 
        Тест на Get после изменения
        """

        user_patch_data = {
            "email": "unique.mail.5@qaguru.autotest",
            "first_name": "UniqueFirstName5",
            "last_name": "UniqueLastName5",
            "avatar": "https://reqres.in/img/faces/unique-avatar-5.jpg"
        }
        
        user: dict = random.choice(users)
        response = requests.patch(f"{app_url}/api/users/{user['id']}", json=user_patch_data)
        assert response.status_code == HTTPStatus.OK   
        updated_user: dict = response.json()
        user_id = updated_user.pop("id", None)
        assert updated_user == user_patch_data
        
        response = requests.get(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        get_user: dict = response.json()
        get_user_id = get_user.pop("id", None)
        assert user_id == get_user_id
        assert get_user == updated_user
    
    @pytest.mark.parametrize("request_data", [
        {
            "method": "GET", 
            "endpoint": "api/users/bulk_delete/"
        },
        {
            "method": "POST",
            "endpoint": "api/users/5"
        }
    ])
    def test_users_method_not_allowed(self, app_url: str, request_data: dict):
        """ 
        Тест на 405 ошибку. Предусловия: ничего не нужно
        """
        
        response = requests.request(method=request_data["method"], url=f"{app_url}/{request_data['endpoint']}")
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
    
    @pytest.mark.parametrize("request_data", [
        {
            "method": "DELETE",
            "json": None
        },
        {
            "method": "PATCH",
            "json": {
                "email": "unique.mail.10@qaguru.autotest"
            }
        }
    ])
    def test_users_method_not_found(self, app_url: str, users: list[User], request_data: dict):
        """ 
        Тест на 404 ошибку при удалении и обновлении
        """
        user_ids = [user["id"] for user in users]
        non_existent_user_id = max(user_ids) + 100
        response = requests.request(
            method=request_data["method"], 
            url=f"{app_url}/api/users/{non_existent_user_id}", 
            json=request_data["json"]
        )
        assert response.status_code == HTTPStatus.NOT_FOUND
        
    @pytest.mark.parametrize("request_data", [
        {
            "method": "DELETE",
            "endpoint": "api/users/0",
            "json": None
        },
        {
            "method": "DELETE",
            "endpoint": "api/users/None",
            "json": None
        },
        {
            "method": "PATCH",
            "endpoint": None,
            "json": {
                "email": 1
            }
        },
        {
            "method": "PATCH",
            "endpoint": None,
            "json": {
                "first_name": [55],
                "last_name": {"test": None}
            }
        }
    ])
    def test_users_method_invalid_data(self, app_url: str, users: list[User], request_data: dict):
        """ 
        Тест на 422 ошибку при удалении и обновлении
        """
        
        endpoint = request_data["endpoint"] if request_data["endpoint"] else f"api/users/{users[0]['id']}"
        response = requests.request(method=request_data["method"], url=f"{app_url}/{endpoint}", json=request_data["json"])
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        
    def test_user_not_found_after_delete(self, app_url: str, users: list[User]):
        """ 
        Тест на 404 после удаления
        """

        user: dict = random.choice(users)
        response = requests.delete(f"{app_url}/api/users/{user['id']}")
        assert response.status_code == HTTPStatus.OK   
        response = requests.get(f"{app_url}/api/users/{user['id']}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        
    def test_user_flow(self, app_url: str):
        """ 
        Тест user flow: создаем, читаем, обновляем, удаляем
        """
        
        user_data: dict = generate_user_data()
        response = requests.post(f"{app_url}/api/users/", json=user_data)
        assert response.status_code == HTTPStatus.CREATED
        created_user: dict = response.json()
        created_user_id = created_user.pop("id", None)
        assert created_user == user_data
        
        response = requests.get(f"{app_url}/api/users/{created_user_id}")
        assert response.status_code == HTTPStatus.OK
        get_user: dict = response.json()
        get_user_id = get_user.pop("id", None)
        assert get_user_id == created_user_id
        assert get_user == created_user
        
        user_patch_data: dict = {
            "first_name": "UniqueFirstName7",
            "last_name": "UniqueLastName7"
        }
        response = requests.patch(f"{app_url}/api/users/{get_user_id}", json=user_patch_data)
        assert response.status_code == HTTPStatus.OK   
        updated_user: dict = response.json()
        updated_user_id = updated_user.pop("id", None)
        assert updated_user_id == get_user_id
        for key in user_patch_data.keys():
            assert user_patch_data[key] != user_data[key]
        
        response = requests.delete(f"{app_url}/api/users/{updated_user_id}")
        assert response.status_code == HTTPStatus.OK
        delete_data: dict = response.json()
        assert delete_data["message"] == "User deleted"
    
    @pytest.mark.parametrize("user_data", [
        {
            "email": "qaguru.autotest",
            "first_name": "UniqueFirstName8",
            "last_name": "UniqueLastName8",
            "avatar": "https://reqres.in/img/faces/unique-avatar-8.jpg"
        },
        {
            "email": "unique.mail.9@qaguru.autotest",
            "first_name": "UniqueFirstName9",
            "last_name": "UniqueLastName9",
            "avatar": "hetetepes:/reqres.in/unique-avatar-9.jpg"
        }
    ])
    def test_user_fields_validation(self, app_url: str, users: list[User], user_data: dict):
        """ 
        Проверка валидности тестовых данных (email, url)
        """
        
        user_id = users[0]["id"]
        
        response = requests.post(f"{app_url}/api/users/", json=user_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        
        response = requests.patch(f"{app_url}/api/users/{user_id}", json=user_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        
    @pytest.mark.parametrize("field_to_remove", [
        "email",
        "first_name",
        "last_name",
        "avatar"
    ])
    def test_user_post_without_field(self, app_url: str, field_to_remove: str):
        """ 
        Проверка отправки модели без поля на создание
        """
        
        user_data = generate_user_data()
        user_data.pop(field_to_remove, None)
        response = requests.post(f"{app_url}/api/users/", json=user_data)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY