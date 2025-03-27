from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator
from typing import Self
from app.auth.utils import get_hash_password


class RoomsSchema(BaseModel):
    name: str = Field(ge=2, le=30)
    description: str
    price: int
    services: dict

    model_config = ConfigDict(from_attributes=True)


class HotelsSchema(BaseModel):
    name: str
    location: str
    services: dict
    image_id: int


    model_config = ConfigDict(from_attributes=True)

class HotelsNameSchema(BaseModel):
    name: str


class LandLordsSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class LandlordsRegistrationSchema(LandLordsSchema):
    again_password: str = Field(min_length=4, max_length=100)
    hotel: HotelsSchema

    @model_validator(mode='after')
    def legit_check_passwords_and_pop_again_password(self) -> Self:
        if self.password != self.again_password:
            raise ValueError("Passwords don't match")
        self.password = get_hash_password(self.password)
        del self.again_password

        return self


class LandLordsAddSchema(LandLordsSchema):
    hotels_id: int


