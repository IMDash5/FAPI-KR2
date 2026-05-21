from fastapi import FastAPI, HTTPException, Header
from typing import Optional
import re

app = FastAPI()

def validate_accept_language(accept_language: str) -> bool:
    if not accept_language:
        return False
    
    parts = accept_language.split(',')
    
    for part in parts:
        part = part.strip()
        if ';q=' in part:
            lang, q_value = part.split(';q=')
            try:
                q = float(q_value)
                if not (0 <= q <= 1):
                    return False
            except ValueError:
                return False
        else:
            lang = part
        
        if not re.match(r'^[a-zA-Z]{2,3}(-[a-zA-Z]{2,})?$', lang):
            return False
    
    return True

@app.get("/headers")
async def get_headers(
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    accept_language: Optional[str] = Header(None, alias="Accept-Language")
):
    if not user_agent:
        raise HTTPException(
            status_code=400, 
            detail={"message": "Bad Request", "reason": "User-Agent header is required"}
        )
    
    if not accept_language:
        raise HTTPException(
            status_code=400, 
            detail={"message": "Bad Request", "reason": "Accept-Language header is required"}
        )
    
    if not validate_accept_language(accept_language):
        raise HTTPException(
            status_code=400,
            detail={"message": "Bad Request", "reason": "Invalid Accept-Language format"}
        )
    
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }