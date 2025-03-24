from pydantic import BaseModel, Field

class Hotel(BaseModel):
    address: str
    name: str
    stars: int = Field(ge=1, le=5)