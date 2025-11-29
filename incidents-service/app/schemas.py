from typing import Optional
from pydantic import BaseModel, Field
from .enums import StatusEnum
from datetime import datetime

class IncidentBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)

class IncidentCreate(IncidentBase):
    user_id: int
    status: StatusEnum = StatusEnum.abierta

class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=200)
    status: Optional[StatusEnum] = None
    user_id: int | None = None

class IncidentOut(IncidentBase):
    id: int
    user_id: int
    status: StatusEnum
    created_at: datetime

    class Config:
        orm_mode = True
