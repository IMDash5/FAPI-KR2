from fastapi import FastAPI
from models import UserCreate


app = FastAPI()

@app.post("/create_user")
async def create_user(user: UserCreate):
    return {
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "is_subscribed": user.is_subscribed
    }