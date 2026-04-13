from mock_service.db.task_db_client import TaskDbClient
from mock_service.schemas.task import Task


class GetTaskResolver:
    def __init__(self, task_id: int, db: TaskDbClient):
        self._task_id = task_id
        self._db = db

    def resolve(self) -> Task | None:
        db_entry_task = self._db.get_task(self._task_id)

        if db_entry_task is None:
            return None

        return Task.model_validate(db_entry_task)
