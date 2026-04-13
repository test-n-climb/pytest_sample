from http import HTTPStatus

import allure
import pytest

from src.clients.api_clients.task_api_client import TaskApiClient
from src.schemas.task_api.responses import CreateTaskResponse
from src.test_data_factories.task_api_inputs.create_task_input_factory import CreateTaskInputFactory


@allure.feature("Task API")
@pytest.mark.task_api
class TestCreateTask:

    @allure.story("Create task")
    @pytest.mark.parametrize(
        "build_fn",
        [
            pytest.param("build", id="without_optional_fields"),
            pytest.param("build_with_optional_fields", id="with_optional_fields"),
        ],
    )
    def test_create_task(
        self, task_api_client: TaskApiClient, create_task_input_factory: CreateTaskInputFactory, build_fn: str
    ):
        task_input = getattr(create_task_input_factory, build_fn)()

        response = task_api_client.create_task(task_input)

        assert response.status_code == HTTPStatus.CREATED

        response_body = CreateTaskResponse.model_validate_json(response.text)

        assert response_body.success is True
        assert response_body.data.name == task_input["name"]
        assert response_body.data.text == task_input["text"]
        assert response_body.data.is_completed is False

        get_response = task_api_client.get_task(response_body.data.id)

        assert get_response.status_code == HTTPStatus.OK

        get_response_body = CreateTaskResponse.model_validate_json(get_response.text)

        assert get_response_body.success is True
        assert get_response_body.data.id == response_body.data.id
        assert get_response_body.data.name == task_input["name"]
        assert get_response_body.data.text == task_input["text"]
        assert get_response_body.data.deadline == response_body.data.deadline
        assert get_response_body.data.is_completed == response_body.data.is_completed
        assert get_response_body.data.created_at == response_body.data.created_at
