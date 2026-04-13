from datetime import datetime, timedelta, timezone

from faker import Faker

faker = Faker()


class DatetimeHelpers:

    @staticmethod
    def get_future_date_time_with_format(format_of_date: str, add_days=None) -> str:
        if add_days is None:
            add_days = faker.random_int(min=1, max=31)
        return (datetime.now(timezone.utc) + timedelta(days=add_days)).strftime(format_of_date)

    @staticmethod
    def get_current_date_time_with_format(format_of_date: str) -> str:
        return datetime.now(timezone.utc).strftime(format_of_date)

    @staticmethod
    def get_past_date_time_with_format(format_of_date: str, subtract_days=None) -> str:
        if subtract_days is None:
            subtract_days = faker.random_int(min=1, max=31)
        return (datetime.now(timezone.utc) - timedelta(days=subtract_days)).strftime(format_of_date)
