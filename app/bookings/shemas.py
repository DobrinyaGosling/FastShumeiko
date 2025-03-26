from pydantic import BaseModel, ConfigDict
from datetime import date


class Bookings(BaseModel):
    date_from: date
    date_to: date


    model_config = ConfigDict(from_attributes=True)