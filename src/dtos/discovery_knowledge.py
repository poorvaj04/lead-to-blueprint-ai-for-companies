from dataclasses import dataclass, field

from src.dtos.discovery_topic import (
    DiscoveryTopic,
)


@dataclass
class DiscoveryKnowledge:

    project_type: str

    topics: list[
        DiscoveryTopic
    ] = field(
        default_factory=list
    )