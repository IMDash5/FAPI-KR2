from fastapi import FastAPI, HTTPException, Response, Cookie
from models import LoginData
import uuid
from typing import Optional

app = FastAPI()

VALID_USERS = {
    "user123": "password123",
    "admin": "admin123"
}

sessions = {}

@app.post("/login")
async def login(login_data: LoginData, response: Response):
    if login_data.username in VALID_USERS and VALID_USERS[login_data.username] == login_data.password:
        session_token = str(uuid.uuid4())
        
        sessions[session_token] = login_data.username
        
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=3600,
            secure=False,
            samesite="lax"
        )
        
        return {"message": "Login successful", "session_token": session_token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/user")
async def get_user(session_token: Optional[str] = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})
    
    if session_token in sessions:
        username = sessions[session_token]
        return {
            "message": "User profile",
            "username": username,
            "user_id": session_token
        }
    else:
        raise HTTPException(status_code=401, detail={"message": "Unauthorized"})

