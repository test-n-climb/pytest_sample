from enum import StrEnum


class TestEnvName(StrEnum):
    MOCK = "mock"
    INTEGRATION = "integration"  # for demo purpose, doesn't exist in this set up
    LOCAL = "local"  # for demo purpose, doesn't exist in this set up
