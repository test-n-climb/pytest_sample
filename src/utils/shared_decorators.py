import functools
import logging
import time
from enum import Enum, EnumType
from typing import Callable, TypeVar

T = TypeVar("T")


class SharedDecorators:

    @staticmethod
    def retry(retry_until: Callable[[T], bool] = None, max_retries: int = 3, delay_time: int = 0):
        """
        Retries the decorated function until ``retry_until(result)`` returns True or ``max_retries`` is reached.
        All parameters can be overridden at call time by passing them as keyword arguments to the decorated function.
        """

        def decorator(func):
            @functools.wraps(func)
            def retry_runner(*args, **kwargs):
                retry_until_override = kwargs.get("retry_until")
                max_retries_override = kwargs.get("max_retries")
                delay_time_override = kwargs.get("delay_time")

                if retry_until is None and retry_until_override is None:
                    raise ValueError("No retry_until function is defined")

                retry_until_func = retry_until_override or retry_until
                max_retries_num = max_retries_override or max_retries
                delay_time_sec = delay_time_override or delay_time

                func_kwargs = {k: v for k, v in kwargs.items() if k not in ("retry_until", "max_retries", "delay_time")}

                result: T = None

                for attempt in range(1, max_retries_num + 1):
                    logging.info(f"Running {func.__name__}: attempt {attempt} of {max_retries_num}")

                    result = func(*args, **func_kwargs)

                    if retry_until_func(result):
                        break

                    if attempt < max_retries_num:
                        time.sleep(delay_time_sec)
                else:
                    logging.warning(f"Max retries reached for {func.__name__} without meeting the condition")

                return result

            return retry_runner

        return decorator

    @staticmethod
    def extend_enum(inherited_enums: list[EnumType]):
        """
        extend_enum decorator can be used for an Enum to extend the Enum items with the items of Enums it inherits from.
        """

        def wrapper(added_enum):
            joined = {}
            for inherited_enum in inherited_enums:
                for item in inherited_enum:
                    joined[item.name] = item.value
                for item in added_enum:
                    joined[item.name] = item.value

            base_types = added_enum.__bases__

            return (
                Enum(added_enum.__name__, joined) if len(base_types) > 1 else base_types[0](added_enum.__name__, joined)
            )

        return wrapper
