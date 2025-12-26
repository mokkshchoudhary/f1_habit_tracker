from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitCreate(BaseModel):
    name: str
    description: Optional[str] = None

class HabitResponse(BaseModel):
    id: int
    name:str
    description: Optional[str]
    created_at: datetime
    is_completed_today: bool

    class Config:
        from_attributes = True