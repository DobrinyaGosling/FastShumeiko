from .base import BaseDAO
from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels, Rooms, Landlords

class UsersDAO(BaseDAO):
    model = Users


class BookingsDAO(BaseDAO):
    model = Bookings


class HotelsDAO(BaseDAO):
    model = Hotels


class RoomsDAO(BaseDAO):
    models = Rooms


class LandLordsDAO(BaseDAO):
    model = Landlords