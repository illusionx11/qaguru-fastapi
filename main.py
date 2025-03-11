import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from http import HTTPStatus
from models.User import User
from models.AppStatus import AppStatus
import json
import dotenv
import os

dotenv.load_dotenv()

app = FastAPI()
add_pagination(app)
users: list[User] = []

@app.get("/status/", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users))

@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
    
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    return users[user_id - 1]

@app.get("/api/users/", response_model=Page[User],status_code=HTTPStatus.OK)
def get_users() -> list[User]:
    return paginate(users)

if __name__ == "__main__":
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    
    for user in users:
        User.model_validate(user)
    
    print("Users loaded")
    
    APP_URL = os.getenv("APP_URL").split("http://")[1]
    APP_HOST = APP_URL.split(":")[0]
    APP_PORT = int(APP_URL.split(":")[1])
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)