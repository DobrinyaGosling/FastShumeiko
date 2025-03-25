from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict, field_validator
from typing import Self
from app.auth.utils import get_hash_password

class Email(BaseModel):
    email: EmailStr
    model_config = ConfigDict()


class User(Email):
    password: str = Field(min_length=4, max_length=100)


class UserRegistration(Email):
    password: str = Field(min_length=4, max_length=100)
    again_password: str = Field(min_length=4, max_length=100)

    @model_validator(mode='after')
    def legit_check_passwords_and_pop_again_password(self) -> Self:
        if self.password != self.again_password:
            raise ValueError("Passwords don't match")
        self.password = get_hash_password(self.password)
        del self.again_password

        return self

class Id(BaseModel):
    id: int

