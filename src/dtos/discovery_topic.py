from dataclasses import dataclass, field


@dataclass
class DiscoveryTopic:

    name: str

    goal: str

    expected_items: list[str] = field(
        default_factory=list
    )