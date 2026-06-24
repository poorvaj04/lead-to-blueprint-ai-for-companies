from dataclasses import dataclass, field
from typing import Optional

from src.dtos.conversation_message import (
    ConversationMessage,
)

from src.dtos.speech_result import (
    SpeechResult,
)

from src.dtos.conversation_state import (
    ConversationState,
)

from src.dtos.requirement_fact import (
    RequirementFact,
)


@dataclass
class WorkflowContext:

    # ==================================================
    # Current Speech
    # ==================================================

    speech_result: SpeechResult | None = None

    phase: str = "DISCOVERY" # DISCOVERY, CONFIRMATION, COMPLETED

    # ==================================================
    # Conversation
    # ==================================================

    conversation_history: list[
        ConversationMessage
    ] = field(default_factory=list)

    conversation_state: ConversationState = field(
        default_factory=ConversationState
    )

    questions_asked: int = 0

    # ==================================================
    # Project Discovery
    # ==================================================

    project_understanding = None

    discovery_plan = None

    client_id: Optional[int] = None

    project_name: Optional[str] = None

    is_continuation: bool = False
    
    final_decision: Optional[str] = None

    # ==================================================
    # Knowledge Base
    # ==================================================

    requirement_facts: list[
        RequirementFact
    ] = field(default_factory=list)

    # ==================================================
    # Reception Agent Output
    # ==================================================

    decision: str = ""

    reason: str = ""

    next_question: str = ""

    confidence: int = 0

    # ==================================================
    # Future Agents
    # ==================================================

    requirement_summary: dict = field(
        default_factory=dict
    )

    allocated_resources: dict = field(
        default_factory=dict
    )

    project_estimation: dict = field(
        default_factory=dict
    )

    # ==================================================

    def add_client_message(
        self,
        message: str,
    ):

        self.conversation_history.append(

            ConversationMessage(

                speaker="Client",

                message=message,

            )

        )

    # ==================================================

    def add_ai_message(
        self,
        message: str,
    ):

        self.conversation_history.append(

            ConversationMessage(

                speaker="AI",

                message=message,

            )

        )

    # ==================================================

    def get_conversation_text(self):

        lines = []

        for msg in self.conversation_history:

            lines.append(

                f"{msg.speaker}: {msg.message}"

            )

        return "\n".join(lines)