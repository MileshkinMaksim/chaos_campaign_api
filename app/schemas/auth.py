from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Token(BaseModel):
    """Ответ API с JWT токеном доступа."""
    access_token: str = Field(..., description="JWT токен доступа")
    token_type: str = Field(default="bearer", description="Тип токена")


class TokenData(BaseModel):
    """Данные, зашифрованные внутри JWT токена."""
    commander_id: Optional[str] = Field(None, description="UUID командира в БД")


class UserLogin(BaseModel):
    """Схема входа пользователя."""
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "commander_vance"})
    password: str = Field(..., min_length=4, json_schema_extra={"example": "strongpassword123"})


class UserRegister(BaseModel):
    """Схема регистрации нового командира в СУБД."""
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "commander_vance"})
    password: str = Field(..., min_length=6, json_schema_extra={"example": "strongpassword123"})


class UserResponse(BaseModel):
    """Публичные данные пользователя."""
    id: str = Field(..., description="Уникальный UUID пользователя в БД")
    username: str
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)