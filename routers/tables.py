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
        table_data = ResponseTable(name=name, seats=seats, location=location)
        return await TableService.create_table(db=db, table_data=table_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating table: {e}")

@router.get("/tables/delete", response_class=HTMLResponse)
async def show_delete_table_form(request: Request, db: AsyncSession = Depends(get_db)):
    tables = await TableService.get_all_tables(db)
    return templates.TemplateResponse("delete_tables.html", {"request": request, "tables": tables})

# Роут для обработки удаления стола
@router.post("/tables/delete/{table_id}", response_model=GreatTable)
async def delete_table(
    table_id: int,
    db: AsyncSession = Depends(get_db)
):
    table = await TableService.delete_table(db=db, table_id=table_id)
    if table:
        return table
    else:
        raise HTTPException(status_code=404, detail="Table not found")
