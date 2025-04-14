from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.table_models import Reservation
from models.pydentic_model import ReservationResponse, ReservationGreat

class ReservingService:

    @staticmethod
    async def get_all_reserving(db: AsyncSession) -> list[ReservationGreat]:
        result = await db.execute(select(Reservation))
        tables = result.scalars().all()
        return [ReservationGreat.from_orm(table) for table in tables]

    @staticmethod
    async def create_reservation(
            db: AsyncSession,
            reservation_data: ReservationResponse,
            table_id: int
    ) -> ReservationGreat:
        new_reservation = Reservation(
            customer=reservation_data.customer,
            reservation_time=reservation_data.reservation_time,
            duration_minutes=reservation_data.duration_minutes,
            table_id=table_id
        )

        db.add(new_reservation)
        await db.commit()
        await db.refresh(new_reservation)

        return ReservationGreat.from_orm(new_reservation)
