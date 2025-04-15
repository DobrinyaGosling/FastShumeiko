from datetime import date

from pydantic import BaseModel, ConfigDict


class CreateBookingsSchema(BaseModel):
    date_from: date
    date_to: date
    price: int
    room_id: int
    user_id: int


class UpdateBookingsSchema(BaseModel):
    date_from: date
    date_to: date
    room_id: int

    model_config = ConfigDict(from_attributes=True)

class GetBookingsSchema(BaseModel):
    user_id: int

    model_config = ConfigDict(from_attributes=True)