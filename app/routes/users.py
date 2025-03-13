import os
import sys
sys.path.append(f"{os.getcwd()}/")
from typing import Iterable
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext import sqlmodel
from app.models.User import User, UserCreate, UserUpdate
from app.database import users
from http import HTTPStatus

router = APIRouter(prefix="/api/users")

@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User | None:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
    user = users.get_user(user_id)
    
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    return user

@router.get("/", response_model=Page[User],status_code=HTTPStatus.OK)
def get_users() -> Iterable[User]:
    return users.get_users()

@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    try:
        UserCreate.model_validate(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    
    return users.create_user(user)

@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
    
    try:
        UserUpdate.model_validate(user.model_dump())
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    
    updated_user = users.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return updated_user

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int) -> dict[str, str]:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
    result = users.delete_user(user_id)
    if not result:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    
    return {"message": "User deleted"}

@router.delete("/bulk_delete/", status_code=HTTPStatus.NO_CONTENT)
def delete_users_bulk(user_ids: dict[str, list[int]]) -> None:
    for user_id in user_ids["ids"]:
        if user_id < 1:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="User ID must be greater than 0")
        users.delete_user(user_id)