from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.auth.utils import get_hash_password


class RoomsSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str
    price: int
    services: dict
    image_id: int | None

    model_config = ConfigDict(from_attributes=True)

class AddRoomsSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str
    price: int
    services: dict
    image_id: int | None
    hotel_id: int

    model_config = ConfigDict(from_attributes=True)


class UpdateRoomsSchema(BaseModel):
    description: str
    price: int
    services: dict
    image_id: int | None

    model_config = ConfigDict(from_attributes=True)


class HotelsSchema(BaseModel):
    name: str
    location: str
    services: dict
    image_id: int | None
    rooms_quantity: int

    model_config = ConfigDict(from_attributes=True)



class UpdateHotelsSchema(BaseModel):
    services: dict
    rooms_quantity: int
    image_id: int | None

    model_config = ConfigDict(from_attributes=True)


class StrSchema(BaseModel):
    name: str

class IntIntSchema(BaseModel):
    id: int
    hotel_id: int


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


