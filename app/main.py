import os
import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from routes import status, users
from models.User import User
from database import users_db
import json
import dotenv

dotenv.load_dotenv()

app = FastAPI()
app.include_router(status.router)
app.include_router(users.router)
add_pagination(app)

if __name__ == "__main__":
    with open("users.json", "r", encoding="utf-8") as f:
        users_db.extend(json.load(f))
    
    for user in users_db:
        User.model_validate(user)
    
    print("Users loaded")
    
    APP_URL = os.getenv("APP_URL").split("http://")[1]
    APP_HOST = APP_URL.split(":")[0]
    APP_PORT = int(APP_URL.split(":")[1])
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)