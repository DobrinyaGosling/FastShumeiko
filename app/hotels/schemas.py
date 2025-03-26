from pydantic import BaseModel, Field, EmailStr, ConfigDict



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
    rooms_quantity: int
    image_id: int
    rooms: list[RoomsSchema]

    model_config = ConfigDict(from_attributes=True)



class LandlordsSchema(BaseModel):
    email: EmailStr
    hotel: HotelsSchema

    model_config = ConfigDict(from_attributes=True)
