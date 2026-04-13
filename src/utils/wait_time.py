from enum import Enum


class WaitTime(float, Enum):
    EXTRA_LARGE = 10
    LARGE = 5
    MEDIUM = 2.5
    SMALL = 1
    EXTRA_SMALL = 0.5
