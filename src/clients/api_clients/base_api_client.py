from abc import ABC
from enum import StrEnum
from typing import Callable

from requests import Response, request

from src.clients.api_clients.api_call_interceptor import ApiCallInterceptor

DEFAULT_RETRY_NUMBER = 7


class SupportedMethod(StrEnum):
    POST = "POST"
    GET = "GET"


class BaseApiClient(ABC):
    """Abstract base for API clients. Provides methods with built-in retry and logging via ApiCallInterceptor."""

    def __init__(
        self,
        base_url: str,
        base_headers: dict,
        default_delay_time: int | float = None,
        default_max_retries: int = None,
    ):
        self.base_url: str = base_url
        self.base_headers: dict = base_headers
        self.default_delay_time: int | float = default_delay_time
        self.default_max_retries: int = default_max_retries or DEFAULT_RETRY_NUMBER

    @ApiCallInterceptor.process_request(method_name=SupportedMethod.POST)
    def post(
        self,
        endpoint: str,
        data: str | dict = None,
        headers: dict = None,
        params: dict = None,
        is_response_expected: Callable[[Response], bool] = None,
        max_retries: int = None,
        delay_time: int | float = None,
    ) -> Response:
        return request("POST", self.base_url + endpoint, data=data, params=params, headers=headers)

    @ApiCallInterceptor.process_request(method_name=SupportedMethod.GET)
    def get(
        self,
        endpoint: str,
        headers: dict = None,
        params: dict = None,
        is_response_expected: Callable[[Response], bool] = None,
        max_retries: int = None,
        delay_time: int | float = None,
    ) -> Response:
        return request("GET", self.base_url + endpoint, params=params, headers=headers)
