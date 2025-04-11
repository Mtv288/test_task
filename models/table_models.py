from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class BASE(DeclarativeBase):
    pass


class Table(BASE):

    __tablename__  = "table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]

    reservation: Mapped["Reservation"] = relationship(
        "Reservation", back_populates="table",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'{self.name}, {self.seats}, {self.location}'


class Reservation(BASE):

    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str]
    table_id: Mapped[int] = mapped_column(ForeignKey("table.id"))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]

    table: Mapped["Table"] = relationship(
        "Table", back_populates="reservation",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'{self.customer}. {self.table_id}, {self.reservation_time}, {self.duration_minutes}'

