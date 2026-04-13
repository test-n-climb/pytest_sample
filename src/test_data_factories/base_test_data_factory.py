from abc import ABC, abstractmethod
from typing import Any

from faker import Faker

from src.test_data_factories.factory_toolkit import FactoryToolkit


class BaseTestDataFactory(ABC):
    def __init__(self, locale: str | None = None):
        self.locale: str | None = locale
        self.faker: Faker = Faker(locale)

    @abstractmethod
    def get_defaults(self) -> dict[str, Any]:
        pass

    def get_optional_fields(self) -> dict[str, Any]:
        return {}

    @FactoryToolkit.obj_none_to_empty_dict
    def build(self, obj=None) -> dict[str, Any]:
        return FactoryToolkit.deep_merge(self.get_defaults(), obj)

    @FactoryToolkit.obj_none_to_empty_dict
    def build_with_optional_fields(self, obj=None) -> dict[str, Any]:
        base = FactoryToolkit.deep_merge(self.get_defaults(), self.get_optional_fields())
        return FactoryToolkit.deep_merge(base, obj)
