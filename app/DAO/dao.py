from app.bookings.models import Bookings
from app.hotels.models import Hotels, Landlords, Rooms
from app.users.models import Users

from .base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users


class BookingsDAO(BaseDAO):
    model = Bookings


class HotelsDAO(BaseDAO):
    model = Hotels


class RoomsDAO(BaseDAO):
    model = Rooms


class LandLordsDAO(BaseDAO):
    model = Landlords