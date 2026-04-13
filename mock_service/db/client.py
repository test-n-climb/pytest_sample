from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from mock_service.db.base import Base
from mock_service.db.models import Task
from mock_service.schemas.task import PostTaskInput


class DbClient:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        self._internal_client = None
        self._engine = None
        self._initialize_internal_client()

    def _initialize_internal_client(self) -> None:
        if not self._internal_client:
            engine = create_engine(
                "sqlite:///:memory:", echo=True, connect_args={"check_same_thread": False}, poolclass=StaticPool
            )
            Base.metadata.create_all(engine)
            self._internal_client = Session(engine)

    def add_task(self, post_task_input: PostTaskInput) -> Task:
        task = Task(**post_task_input.dict())
        self._internal_client.add(task)
        self._internal_client.commit()
        self._internal_client.refresh(task)

        return task
