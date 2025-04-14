from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from models.pydentic_model import GreatTable, ResponseTable
from models.db_main import get_db
from servises.tables import TableService

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["Tables"])

@router.get("/tables", response_model=list[GreatTable])
async def get_all_tables(db: AsyncSession = Depends(get_db)):
    return await TableService.get_all_tables(db)


@router.get("/tables/new", response_class=HTMLResponse)
async def show_create_table_form(request: Request):
    return templates.TemplateResponse("tables.html", {"request": request})

@router.post("/tables/new", response_model=GreatTable)
async def create_table(
    name: str = Form(...),
    seats: int = Form(...),
    location: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Создание нового стола с переданными данными из формы
        table_data = ResponseTable(name=name, seats=seats, location=location)
        return await TableService.create_table(db=db, table_data=table_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating table: {e}")