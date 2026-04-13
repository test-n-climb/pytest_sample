import logging
from typing import Generator

import allure
import pytest
from dotenv import load_dotenv

from config.config import Config
from config.environment import TestEnvName
from src.clients.api_clients.task_api_client import TaskApiClient
from src.test_data_factories.task_api_inputs.create_task_input_factory import CreateTaskInputFactory
from src.utils.helpers.datatypes.list_helpers import ListHelpers


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        help=f"Environment for the test run. One of: {ListHelpers.list_from_enum_values(TestEnvName)}",
    )


def pytest_sessionstart(session):
    env: str = session.config.getoption("--env")
    if env:
        load_dotenv(dotenv_path=".env." + env.replace("_", "."))

    Config(env_name=env)


@pytest.fixture(scope="session")
@allure.title("Set TaskApiClient")
def task_api_client() -> TaskApiClient:
    return TaskApiClient(Config().base_url)


@pytest.fixture
@allure.title("Set CreateTaskInputFactory")
def create_task_input_factory() -> CreateTaskInputFactory:
    return CreateTaskInputFactory()


@pytest.fixture(autouse=True)
def log_start_and_end(request) -> Generator[None, None, None]:
    logging.info(f"Starting the test: {request.node.name}")
    yield
    logging.info(f"Completing a test: {request.node.name}")
