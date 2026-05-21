from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, description="Имя пользователя")
    email: str = Field(..., description="Email")
    age: Optional[int] = Field(None, description="Возраст")
    is_subscribed: bool = Field(False, description="Подписка на рассылку")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Некорректный формат email")
        return v

    @field_validator("age")
    @classmethod
    def validate_age(cls, v):
        if v and v < 0:
            raise ValueError("Возраст не может быть отрицательным")
        return v