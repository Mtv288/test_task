from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.table_models import Table
from models.pydentic_model import ResponseTable, GreatTable

class TableService:

    @staticmethod
    async def get_all_tables(db: AsyncSession) -> list[GreatTable]:
        result = await db.execute(select(Table))
        tables = result.scalars().all()
        return [GreatTable.from_orm(table) for table in tables]

    @staticmethod
    async def create_table(db: AsyncSession, table_data: ResponseTable) -> GreatTable:
        new_table = Table(
            name=table_data.name,
            seats=table_data.seats,
            location=table_data.location
        )

        db.add(new_table)
        await db.commit()
        await db.refresh(new_table)

        return GreatTable.from_orm(new_table)

    @staticmethod
    async def delete_table(db: AsyncSession, table_id: int) -> GreatTable:
        table = await db.get(Table, table_id)
        if table:
            await db.delete(table)
            await db.commit()
            return GreatTable.from_orm(table)
        return None
