from pydantic import BaseModel, field_validator
from fastapi import HTTPException, Header
import re

class CommonHeaders(BaseModel):
    user_agent: str = Header(..., alias="User-Agent")
    accept_language: str = Header(..., alias="Accept-Language")
    
    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, v: str) -> str:
        if not v:
            raise HTTPException(
                status_code=400,
                detail={"message": "Bad Request", "reason": "Accept-Language header is required"}
            )
        
        parts = v.split(',')
        
        for part in parts:
            part = part.strip()
            if ';q=' in part:
                lang, q_value = part.split(';q=')
                try:
                    q = float(q_value)
                    if not (0 <= q <= 1):
                        raise ValueError
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail={"message": "Bad Request", "reason": f"Invalid q-value in Accept-Language: {q_value}"}
                    )
            else:
                lang = part
            
            if not re.match(r'^[a-zA-Z]{2,3}(-[a-zA-Z]{2,})?$', lang):
                raise HTTPException(
                    status_code=400,
                    detail={"message": "Bad Request", "reason": f"Invalid language format in Accept-Language: {lang}"}
                )
        
        return v