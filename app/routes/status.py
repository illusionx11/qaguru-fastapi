import os
import sys
sys.path.append(f"{os.getcwd()}/")
from fastapi import APIRouter
from app.models.AppStatus import AppStatus
from app.database import users_db
from http import HTTPStatus

router = APIRouter()

@router.get("/status/", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(users=bool(users_db))