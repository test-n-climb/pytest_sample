from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from mock_service.db.base import Base
from mock_service.db.base_db_client import BaseDbClient
from mock_service.db.models import Task
from mock_service.schemas.task import PostTaskInput


class TaskDbClient(BaseDbClient):
    def _initialize_internal_client(self) -> None:
        if not self._internal_client:
            engine = create_engine(
                "sqlite:///:memory:",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )
            Base.metadata.create_all(engine)
            self._internal_client = scoped_session(sessionmaker(bind=engine))

    def add_task(self, post_task_input: PostTaskInput) -> Task:
        task = Task(**post_task_input.dict())
        self._internal_client.add(task)
        self._internal_client.commit()
        self._internal_client.refresh(task)

        return task

    def get_task(self, task_id: int) -> Task | None:
        return self._internal_client.get(Task, task_id)
