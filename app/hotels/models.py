from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[dict] = mapped_column(JSON, nullable=False)
    image_id: Mapped[int] = mapped_column(nullable=False)

    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"), nullable=False)
    hotel: Mapped["Hotels"] = relationship(back_populates="rooms", uselist=False)



class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[dict] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column()

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel", uselist=True, lazy="selectin")
    landlord: Mapped["Landlords"] = relationship(back_populates="hotel", uselist=False, lazy="selectin")



class Landlords(Base):
    __tablename__ = "landlords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    hotels_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    hotel: Mapped["Hotels"] = relationship(back_populates="landlord", uselist=False, lazy="selectin")