from dataclasses import dataclass, field


@dataclass
class TopicGap:

    topic: str

    collected: list[str] = field(
        default_factory=list
    )

    coverage: int = 0

    required: int = 0

    completed: bool = False