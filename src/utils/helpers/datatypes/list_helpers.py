import inspect
import logging
from collections.abc import Iterable
from enum import EnumType
from typing import Callable, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class ListHelpers:

    @staticmethod
    def find(iterable: list[T], func: Callable[[T], bool], default: S = None) -> T | S | None:
        iterable = iterable if isinstance(iterable, Iterable) else []

        def __func(iterable: T) -> bool:
            try:
                return func(iterable)
            except (AttributeError, TypeError):
                logging.warning(f"Failed to apply {inspect.getsource(func)} to {iterable}")

                return False

        return next(filter(__func, iterable), default)

    @staticmethod
    def list_from_enum_values(enum: EnumType) -> list:
        return list(item.value for item in enum)

    @staticmethod
    def list_from_enum_names(enum: EnumType) -> list:
        return list(item.name for item in enum)
