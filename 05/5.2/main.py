from fastapi import FastAPI, HTTPException, Response, Cookie
from itsdangerous import BadSignature, Signer
import uuid
from typing import Optional

from models import LoginData

app = FastAPI()

SECRET_KEY = "my-super-secret-key-12345"
signer = Signer(SECRET_KEY)

VALID_USERS = {
    "user123": "password123",
    "admin": "admin123"
}

@app.post("/login")
def login(login_data: LoginData, response: Response):
    if login_data.username in VALID_USERS and VALID_USERS[login_data.username] == login_data.password:
        user_id = str(uuid.uuid4())
        session_token = signer.sign(user_id).decode("utf-8")

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=3600,
        )
        
        return {
            "message": "Login successful",
            "username": login_data.username,
            "user_id": user_id
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/profile")
def get_profile(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})
    
    try:
        user_id = signer.unsign(session_token).decode("utf-8")

    except (BadSignature, ValueError):
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})
        
    return {
        "message": "Profile information",
        "user_id": user_id,
    }

