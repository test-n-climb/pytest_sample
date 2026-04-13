from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskBase(BaseModel):
    name: str
    text: str
    deadline: Optional[datetime] = None


class PostTaskInput(TaskBase):
    @field_validator("deadline")
    @classmethod
    def validate_deadline(cls, v):
        now = datetime.now()
        if v <= now:
            raise ValueError("deadline must be in the future")
        if v >= now + timedelta(days=100):
            raise ValueError("deadline must be within 100 days from now")
        return v


class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_completed: bool
    created_at: datetime
