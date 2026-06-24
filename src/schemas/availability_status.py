from enum import Enum


class AvailabilityStatus(str, Enum):
    AVAILABLE = "Available"
    PARTIALLY_AVAILABLE = "Partially Available"
    UNAVAILABLE = "Unavailable"