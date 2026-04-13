from abc import ABC, abstractmethod


class BaseDbClient(ABC):
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls._instances.get(cls) is None:
            instance = super(BaseDbClient, cls).__new__(cls)
            instance._internal_client = None
            cls._instances[cls] = instance

        return BaseDbClient._instances[cls]

    def __init__(self):
        self._initialize_internal_client()

    @abstractmethod
    def _initialize_internal_client(self) -> None:
        pass

    def remove(self) -> None:
        self._internal_client.remove()
