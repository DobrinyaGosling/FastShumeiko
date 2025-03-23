from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from typing import Self


class Email(BaseModel):
    email: EmailStr
    model_config = ConfigDict()


class User(Email):
    username: str = Field(min_length=3, max_length=30)

