from enum import StrEnum

from requests import Response

from src.clients.api_clients.base_api_client import BaseApiClient


class TaskApiEndpoint(StrEnum):
    CREATE = "/task/create"
    GET = "/task/{task_id}"


class TaskApiClient(BaseApiClient):
    def __init__(self, base_url: str):
        super().__init__(
            base_url=base_url,
            base_headers={"Content-Type": "application/json"},
        )

    def create_task(self, task_input: dict) -> Response:
        return self.post(endpoint=TaskApiEndpoint.CREATE, data=task_input)

    def get_task(self, task_id: int) -> Response:
        return self.get(endpoint=TaskApiEndpoint.GET.format(task_id=task_id))
