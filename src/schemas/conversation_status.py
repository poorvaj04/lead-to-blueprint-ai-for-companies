from enum import Enum


class ConversationStatus(str, Enum):
    STARTED = "Started"
    RECORDING = "Recording"
    AWAITING_CONFIRMATION = "Awaiting Confirmation"
    CONFIRMED = "Confirmed"
    COMPLETED = "Completed"