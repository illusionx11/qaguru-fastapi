import dotenv
dotenv.find_dotenv()

import os
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.routes import status, users
from app.database.engine import create_db_and_tables

@asynccontextmanager
async def lifespan(_: FastAPI):
    logging.warning("On startup")
    create_db_and_tables()
    yield
    logging.warning("On shutdown")

app = FastAPI(lifespan=lifespan)
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)

if __name__ == "__main__":
    APP_URL = os.getenv("APP_URL").split("http://")[1]
    APP_HOST = APP_URL.split(":")[0]
    APP_PORT = int(APP_URL.split(":")[1])
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
