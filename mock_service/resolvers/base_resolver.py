from abc import ABC, abstractmethod

from pydantic import BaseModel

from mock_service.db.base_db_client import BaseDbClient


class BaseResolver(ABC):
    def __init__(self, event: BaseModel, db: BaseDbClient):
        self._event = event
        self._db = db

    @abstractmethod
    def resolve(self):
        pass
