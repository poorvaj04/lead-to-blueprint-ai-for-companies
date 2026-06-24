from dataclasses import dataclass, field


@dataclass
class ConversationState:

    # ----------------------------

    current_topic_index: int = 0

    # ----------------------------

    current_question: str = ""

    # ----------------------------

    collected_information: list[str] = field(
        default_factory=list
    )

    # ----------------------------

    completed_topics: list[int] = field(
        default_factory=list
    )

    # ----------------------------

    interview_completed: bool = False