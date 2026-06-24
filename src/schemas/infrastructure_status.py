from enum import Enum


class InfrastructureStatus(str, Enum):
    AVAILABLE = "Available"
    LIMITED = "Limited"
    UNAVAILABLE = "Unavailable"