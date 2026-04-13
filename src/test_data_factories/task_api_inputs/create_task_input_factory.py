from typing import Any

from src.test_data_factories.base_test_data_factory import BaseTestDataFactory
from src.utils.helpers.datatypes.datetime_helpers import DatetimeHelpers

_DATE_FORMAT = "%Y-%m-%d"
_DEADLINE_MIN_DAYS = 1
_DEADLINE_MAX_DAYS = 99


class CreateTaskInputFactory(BaseTestDataFactory):

    def get_defaults(self) -> dict[str, Any]:
        return {
            "name": self.faker.word(),
            "text": self.faker.sentence(),
        }

    def get_optional_fields(self) -> dict[str, Any]:
        return {
            "deadline": DatetimeHelpers.get_future_date_time_with_format(
                format_of_date=_DATE_FORMAT,
                add_days=self.faker.random_int(min=_DEADLINE_MIN_DAYS, max=_DEADLINE_MAX_DAYS),
            )
        }
