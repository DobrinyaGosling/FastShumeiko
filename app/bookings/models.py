from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Date, Computed


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[str] = mapped_column(Date, nullable=False)
    date_to: Mapped[str] = mapped_column(Date, nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    total_cost: Mapped[int] = mapped_column(Computed((date_to - date_from)*price))
    total_days: Mapped[int] = mapped_column(Computed(date_to - date_from))