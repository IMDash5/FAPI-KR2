from fastapi import FastAPI, HTTPException, Response, Cookie, Request
from itsdangerous import BadSignature, Signer
import uuid
from typing import Optional
import time
from models import LoginData


app = FastAPI()

SECRET_KEY = "my-super-secret-key-12345"
TOKEN_LIFETIME = 300
REFRESH_AFTER = 180

signer = Signer(SECRET_KEY)

VALID_USERS = {
    "user123": "password123",
    "admin": "admin123"
}

def create_session_token(user_id: str, timestamp: int) -> str:
    value = f"{user_id}.{timestamp}"
    return signer.sign(value).decode("utf-8")

def parse_session_token(token: str) -> tuple[str, int]:
    try:
        decoded = signer.unsign(token).decode("utf-8")
        user_id, timestamp_str = decoded.rsplit(".", 1)
        timestamp = int(timestamp_str)
        return user_id, timestamp
    except (BadSignature, ValueError, AttributeError):
        raise HTTPException(status_code=401, detail={"message": "Invalid session"})

def should_refresh_session(last_activity: int) -> bool:
    current_time = int(time.time())
    time_passed = current_time - last_activity
    
    if REFRESH_AFTER <= time_passed < TOKEN_LIFETIME:
        return True
    elif time_passed >= TOKEN_LIFETIME:
        raise HTTPException(status_code=401, detail={"message": "Session expired"})
    else:
        return False

def update_session_cookie(response: Response, user_id: str, new_timestamp: int):
    new_token = create_session_token(user_id, new_timestamp)
    response.set_cookie(
        key="session_token",
        value=new_token,
        httponly=True,
        max_age=TOKEN_LIFETIME,
        secure=False,
    )

@app.post("/login")
def login(login_data: LoginData, response: Response):
    if login_data.username in VALID_USERS and VALID_USERS[login_data.username] == login_data.password:
        user_id = str(uuid.uuid4())
        current_time = int(time.time())
        session_token = create_session_token(user_id, current_time)

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            max_age=TOKEN_LIFETIME,
            secure=False,
        )
        
        return {
            "message": "Login successful",
            "username": login_data.username,
            "user_id": user_id
        }
    else:
        raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})

@app.get("/profile")
def get_profile(
    request: Request,
    response: Response,
    session_token: Optional[str] = Cookie(None)
):
    if not session_token:
        raise HTTPException(status_code=401, detail={"message": "Session expired"})
    
    user_id, last_activity = parse_session_token(session_token)
    
    current_time = int(time.time())
    time_passed = current_time - last_activity
    
    if time_passed >= TOKEN_LIFETIME:
        raise HTTPException(status_code=401, detail={"message": "Session expired"})
    
    if time_passed >= REFRESH_AFTER:
        update_session_cookie(response, user_id, current_time)
    
    return {
        "message": "Profile information",
        "user_id": user_id,
        "last_activity": last_activity,
        "current_time": current_time,
        "time_passed": time_passed,
        "session_refreshed": time_passed >= REFRESH_AFTER
    }

