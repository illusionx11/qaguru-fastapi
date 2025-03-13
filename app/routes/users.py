import os
import sys
sys.path.append(f"{os.getcwd()}/")
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page, add_pagination, paginate
from app.models.User import User
from app.database import users_db
from http import HTTPStatus

router = APIRouter(prefix="/api/users")

@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
    
    if user_id > len(users_db):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    return users_db[user_id - 1]

@router.get("/", response_model=Page[User],status_code=HTTPStatus.OK)
def get_users() -> list[User]:
    return paginate(users_db)