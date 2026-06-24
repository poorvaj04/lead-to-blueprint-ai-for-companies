from dataclasses import dataclass, field

from src.dtos.discovery_topic import (
    DiscoveryTopic,
)


@dataclass
class DiscoveryPlan:

    project_title: str = ""

    overall_goal: str = ""

    topics: list[DiscoveryTopic] = field(
        default_factory=list
    )

    def completed_topics(self):

        return sum(

            topic.completed

            for topic in self.topics

        )

    def total_topics(self):

        return len(self.topics)

    def next_pending_topic(self):

        for topic in self.topics:

            if not topic.completed:

                return topic

        return None