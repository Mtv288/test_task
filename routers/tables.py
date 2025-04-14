from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.responses import HTMLResponse
from models.pydentic_model import GreatTable, ResponseTable
from models.db_main import get_db
from servises.tables import TableService

router = APIRouter(tags=["Tables"])

@router.get("/tables", response_model=list[GreatTable])
async def get_all_tables(db: AsyncSession = Depends(get_db)):
    return await TableService.get_all_tables(db)