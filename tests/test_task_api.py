from http import HTTPStatus

import allure
import pytest

from src.clients.api_clients.task_api_client import TaskApiClient
from src.schemas.task_api.responses import CreateTaskResponse, TaskApiErrors
from src.test_data_factories.task_api_inputs.create_task_input_factory import CreateTaskInputFactory
from src.utils.helpers.datatypes.datetime_helpers import DatetimeHelpers

_DATE_FORMAT = "%Y-%m-%d"


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

    @allure.story("Create task with invalid deadline")
    @pytest.mark.parametrize(
        "deadline, expected_error",
        [
            pytest.param(
                DatetimeHelpers.get_past_date_time_with_format(_DATE_FORMAT, subtract_days=1),
                TaskApiErrors.DEADLINE_IN_PAST,
                id="past_deadline",
            ),
            pytest.param(
                DatetimeHelpers.get_future_date_time_with_format(_DATE_FORMAT, add_days=101),
                TaskApiErrors.DEADLINE_TOO_FAR,
                id="over_100_days",
            ),
        ],
    )
    def test_create_task_with_invalid_deadline(
        self,
        task_api_client: TaskApiClient,
        create_task_input_factory: CreateTaskInputFactory,
        deadline: str,
        expected_error: TaskApiErrors,
    ):
        task_input = create_task_input_factory.build({"deadline": deadline})

        response = task_api_client.create_task(task_input)

        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

        response_body = CreateTaskResponse.model_validate_json(response.text)

        assert response_body.success is False
        assert response_body.data is None
        assert response_body.errors is not None
        assert response_body.errors[0].msg == expected_error
