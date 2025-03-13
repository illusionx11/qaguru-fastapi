from typing import Iterable, Type
from sqlmodel import Session, select
from fastapi_pagination.ext import sqlmodel
from .engine import engine
from app.models.User import User, UserCreate, UserUpdate
from fastapi import HTTPException

def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)
    
def get_users() -> Iterable[User]:
    with Session(engine) as session:
        statement = select(User)
        return sqlmodel.paginate(session, statement)
    
def create_user(user: User) -> User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def update_user(user_id: int, user: User) -> Type[User] | None:
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            return None
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    
def delete_user(user_id: int) -> bool | None:
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            return None
        session.delete(user)
        session.commit()
        return True