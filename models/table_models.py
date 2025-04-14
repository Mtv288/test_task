from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

class Base(DeclarativeBase):
    pass


class Table(Base):
    __tablename__ = "table"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    seats: Mapped[int]
    location: Mapped[str]

    # Связь с Reservation, каскадное удаление настроено на стороне "одного" (Table)
    reservation: Mapped["Reservation"] = relationship(
        "Reservation", back_populates="table", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.seats}, {self.location}'


class Reservation(Base):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer: Mapped[str]
    table_id: Mapped[int] = mapped_column(ForeignKey("table.id"))
    reservation_time: Mapped[datetime]
    duration_minutes: Mapped[int]

    # Связь с Table, на стороне "многих" не должно быть каскадного удаления
    table: Mapped["Table"] = relationship(
        "Table", back_populates="reservation", single_parent=True
    )

    def __repr__(self):
        return f'{self.customer}. {self.table_id}, {self.reservation_time}, {self.duration_minutes}'
