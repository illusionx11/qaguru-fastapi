from requests import Response
from tests.config import Server
from tests.utils.base_session import BaseSession

class APIWrapper:
    def __init__(self, env, **kwargs):
        self.session = BaseSession(base_url=Server(env).app)
    
    def _apicall(self, method, url, *args, **kwargs):
        return self.session.request(method, url, *args, **kwargs)
    
    def get_status(self) -> Response:
        return self.session.get(f"/status/")
    
    def get_user(self, user_id: int) -> Response:
        return self.session.get(f"/api/users/{user_id}")
    
    def get_users(self, params: dict | None = None) -> Response:
        return self.session.get(f"/api/users/", params=params)
    
    def create_user(self, user_data: dict | None = None) -> Response:
        return self.session.post(f"/api/users/", json=user_data)
    
    def update_user(self, user_id: int, user_data: dict | None = None) -> Response:
        return self.session.patch(f"/api/users/{user_id}", json=user_data)
    
    def delete_user(self, user_id: int) -> Response:
        return self.session.delete(f"/api/users/{user_id}")
    
    def delete_users_bulk(self, user_ids: list[int]) -> Response:
        return self.session.delete(f"/api/users/bulk_delete/", json={"ids": user_ids})