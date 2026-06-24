from enum import Enum


class ProjectStatus(str, Enum):
    SUCCESSFULLY_COMPLETED = "Successfully Completed"
    PARTIALLY_COMPLETED = "Partially Completed"
    CANCELLED = "Cancelled"