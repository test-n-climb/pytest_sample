from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.sql.sqltypes import TIMESTAMP

from mock_service.db.base import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    text = Column(String, nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=True, server_default=None)
    is_completed = Column(Boolean, nullable=False, default=False, server_default="false")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
