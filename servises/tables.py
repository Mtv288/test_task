from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from models.table_models import Table
from models.pydentic_model import ResponseTable, GreatTable

class TableService:

    @staticmethod
    async def get_all_tables(db: AsyncSession) -> list[GreatTable]:
        result = await db.execute(select(Table))
        tables = result.scalars().all()
        return [GreatTable.from_orm(table) for table in tables]