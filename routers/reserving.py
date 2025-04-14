from datetime import datetime
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from models.pydentic_model import ReservationGreat, ReservationResponse
from models.db_main import get_db
from servises.reserving import ReservingService
from servises.tables import TableService

templates = Jinja2Templates(directory="templates")
router = APIRouter(tags=["Reserving"])

@router.get("/reservations", response_model=list[ReservationGreat])
async def get_all_reservation(db: AsyncSession = Depends(get_db)):
    return await ReservingService.get_all_reserving(db)

@router.get("/reservations/new", response_class=HTMLResponse)
async def show_create_reservation_form(request: Request, db: AsyncSession = Depends(get_db)):
    tables = await TableService.get_all_tables(db)
    return templates.TemplateResponse("create_reservation.html", {"request": request, "tables": tables})

@router.post("/reservations/new", response_model=ReservationGreat)
async def create_reservation(
    customer: str = Form(...),
    table_id: int = Form(...),
    reservation_time: str = Form(...),
    duration_minutes: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        from datetime import datetime
        reservation_time = datetime.fromisoformat(reservation_time)

        reservation_data = ReservationResponse(
            customer=customer,
            reservation_time=reservation_time,
            duration_minutes=duration_minutes
        )

        return await ReservingService.create_reservation(db, reservation_data, table_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании брони: {e}")


@router.get("/reservations/delete", response_class=HTMLResponse)
async def show_delete_reservation_page(request: Request, db: AsyncSession = Depends(get_db)):
    reservations = await ReservingService.get_all_reserving(db)
    return templates.TemplateResponse("delete_reservation.html", {
        "request": request,
        "reservations": reservations
    })


@router.post("/reservations/delete/{reservation_id}")
async def delete_reservation(reservation_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await ReservingService.delete_reservation(db, reservation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Бронь не найдена")
    return RedirectResponse(url="/reservations/delete", status_code=303)
