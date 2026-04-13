from mock_service.db.task_db_client import TaskDbClient
from mock_service.resolvers.base_resolver import BaseResolver
from mock_service.schemas.task import PostTaskInput, Task


class CreateTaskResolver(BaseResolver):
    def __init__(self, event: PostTaskInput, db: TaskDbClient):
        super().__init__(event, db)
        self._event = event
        self._db = db

    def resolve(self) -> Task:
        db_entry_task = self._db.add_task(self._event)

        return Task.model_validate(db_entry_task)
