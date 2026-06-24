from dataclasses import dataclass


@dataclass
class ConversationMessage:

    speaker: str

    message: str