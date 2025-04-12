from pydantic import BaseModel
from datetime import datetime


class GreatTable(BaseModel):
    id: int
    name: str
    seats: int
    location: str

    class Config:
        orm_mode = True


class ResponseTable(BaseModel):
    name: str
    seats: int
    location: str

    class Config:
        orm_mode = True


class ReservationGreat(BaseModel):
    id: int
    customer: str
    reservation_time: datetime
    duration_minutes: int

    class Config:
        orm_mode = True


class ReservationResponse(BaseModel):
    customer: str
    reservation_time: datetime
    duration_minutes: int

    class Config:
        orm_mode = True