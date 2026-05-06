from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

BCRYPT_MAX_PASSWORD_BYTES = 72


def _password_within_bcrypt_limit(password: str) -> str:
    if len(password.encode("utf-8")) > BCRYPT_MAX_PASSWORD_BYTES:
        msg = (
            "Пароль не может быть длиннее "
            f"{BCRYPT_MAX_PASSWORD_BYTES} байт в UTF-8 (ограничение bcrypt)"
        )
        raise ValueError(msg)
    return password


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=1, max_length=255)
    role: Literal["customer", "courier"] = "customer"

    @field_validator("password")
    @classmethod
    def password_utf8_byte_limit(cls, value: str) -> str:
        return _password_within_bcrypt_limit(value)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

    @field_validator("password")
    @classmethod
    def password_utf8_byte_limit(cls, value: str) -> str:
        return _password_within_bcrypt_limit(value)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
