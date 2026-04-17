from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel


class Task(BaseModel):
    id: int
    name: str
    text: str
    deadline: Optional[datetime] = None
    is_completed: bool
    created_at: datetime


class TaskApiErrors(StrEnum):
    DEADLINE_IN_PAST = "Value error, deadline must be in the future"
    DEADLINE_TOO_FAR = "Value error, deadline must be within 100 days from now"


class ValidationError(BaseModel):
    type: str
    loc: list[str | int]
    msg: str
    input: Optional[Any] = None


class CreateTaskResponse(BaseModel):
    success: bool
    errors: Optional[list[ValidationError]] = None
    data: Optional[Task] = None
