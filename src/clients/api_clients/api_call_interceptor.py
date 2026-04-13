import functools
import json
import logging
from copy import deepcopy
from http import HTTPStatus
from typing import Callable

from requests import Response

from src.utils.json_pattern import JSON_PATTERN
from src.utils.shared_decorators import SharedDecorators


class ApiCallInterceptor:
    """Wraps BaseApiClient HTTP methods with request/response logging and configurable retry logic."""

    @staticmethod
    def process_request(method_name):
        def decorator(func):
            @functools.wraps(func)
            def wrap(api_client, **kwargs):
                # get arguments from kwargs or set to default
                endpoint = kwargs.get("endpoint")
                headers = api_client.base_headers

                if kwargs.get("headers"):
                    headers = {**headers, **kwargs.get("headers")}

                params = kwargs.get("params")
                data = kwargs.get("data")

                max_retries = kwargs.get("max_retries") or api_client.default_max_retries
                delay_time = kwargs.get("delay_time") or api_client.default_delay_time

                is_response_expected = kwargs.get("is_response_expected")

                retry_until = ApiCallInterceptor._define_retry_until(is_response_expected)

                ApiCallInterceptor._log_request(method_name, endpoint, headers, data, params)

                # make an API call with set retry params and get response
                response = ApiCallInterceptor._make_api_call(
                    func,
                    api_client=api_client,
                    endpoint=endpoint,
                    headers=headers,
                    params=params,
                    data=data,
                    retry_until=retry_until,
                    max_retries=max_retries,
                    delay_time=delay_time,
                )

                ApiCallInterceptor._log_response(method_name, endpoint, response)

                return response

            return wrap

        return decorator

    @staticmethod
    def _log_request(
        method_name: str, endpoint: str, headers: dict, data: dict | str = None, params: dict = None
    ) -> None:
        headers_to_log = deepcopy(headers)

        # if there is an Authorization header with JWT, not logging full JWT to reduce log side
        if headers_to_log.get("Authorization") and "Bearer" in headers_to_log.get("Authorization"):
            headers_to_log["Authorization"] = headers_to_log["Authorization"][0:20] + "...{jwt}"

        message = f"Calling {method_name} {endpoint} with \n" f"Headers:\n{json.dumps(headers_to_log, indent=2)}\n"

        if params:
            message += f"Query params: {json.dumps(params, indent=2)}"

        if data:
            message += f"Body: {json.dumps(data, indent=2, ensure_ascii=False)}"

        logging.info(message)

    @staticmethod
    def _log_response(method_name: str, endpoint: str, response: Response) -> None:
        body = (
            json.dumps(response.json(), indent=2, ensure_ascii=False)
            if bool(JSON_PATTERN.match(response.text))
            else response.text
        )

        logging.info(
            f"{method_name} {endpoint} responded with:\n" f"Status code: {response.status_code}\n" f"Body: {body}"
        )

    @staticmethod
    def is_response_ok(response: Response):
        return response.ok

    @staticmethod
    def is_client_error(response: Response) -> bool:
        if HTTPStatus(response.status_code).is_client_error:
            logging.warning(f"Received status code: {response.status_code}. Stop retrying.")
            return True
        return False

    @staticmethod
    def _define_retry_until(is_response_expected: Callable[[Response], bool] = None) -> Callable[[Response], bool]:
        is_response_expected = is_response_expected or ApiCallInterceptor.is_response_ok

        # will not retry on client error
        def retry_until(response: Response):
            return is_response_expected(response) or ApiCallInterceptor.is_client_error(response)

        return retry_until

    @staticmethod
    @SharedDecorators.retry()
    def _make_api_call(
        func,
        api_client,
        endpoint: str,
        headers: dict,
        params: dict = None,
        data: dict | str = None,
        retry_until: Callable[[Response], bool] = None,
        max_retries: int = None,
        delay_time: int | float = None,
    ) -> Response:
        call_kwargs = dict(endpoint=endpoint, headers=headers, params=params)
        if data is not None:
            call_kwargs["data"] = json.dumps(data) if isinstance(data, dict) else data
        return func(api_client, **call_kwargs)
