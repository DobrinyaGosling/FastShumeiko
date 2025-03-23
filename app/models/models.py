from sqlalchemy import ForeignKey
import json
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[int] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[int] = mapped_column(default=1, nullable=False)


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[json] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column(nullable=False)


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    