import dotenv
dotenv.find_dotenv()

import os
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from routes import status, users
from database.engine import create_db_and_tables

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)

if __name__ == "__main__":
    create_db_and_tables()
    APP_URL = os.getenv("APP_URL").split("http://")[1]
    APP_HOST = APP_URL.split(":")[0]
    APP_PORT = int(APP_URL.split(":")[1])
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)