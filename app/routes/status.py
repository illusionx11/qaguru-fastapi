import os
import sys
sys.path.append(f"{os.getcwd()}/")
from fastapi import APIRouter
from app.models.AppStatus import AppStatus
from app.database.engine import check_availability
from http import HTTPStatus

router = APIRouter()

@router.get("/status/", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_availability())