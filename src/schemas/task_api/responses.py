from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    name: str
    text: str
    deadline: Optional[datetime] = None
    is_completed: bool
    created_at: datetime


class CreateTaskResponse(BaseModel):
    success: bool
    errors: Optional[str] = None
    data: Optional[Task] = None
