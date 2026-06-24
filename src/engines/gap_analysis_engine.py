from src.dtos.topic_gap import (
    TopicGap,
)


class GapAnalysisEngine:

    def __init__(self):

        self.minimum_required = {

            "Business Goals": 2,

            "Current Process": 2,

            "Core Features": 3,

            "Integration Needs": 2,

        }

    # --------------------------------------------------

    def analyze(

        self,

        workflow_context,

        current_topic,

    ) -> TopicGap:

        def normalize_topic(t: str) -> str:
            t = t.lower().strip()
            if t.startswith("module"):
                t = t.split(":", 1)[-1].strip()
            return t

        norm_current = normalize_topic(current_topic)

        facts = [

            fact

            for fact in workflow_context.requirement_facts

            if normalize_topic(fact.topic) == norm_current

        ]

        collected = [

            fact.key

            for fact in facts

        ]

        # Dynamic required count based on expected items to make progress more granular
        required = 4
        if workflow_context.discovery_plan:
            for t in workflow_context.discovery_plan.topics:
                if t.name == current_topic and hasattr(t, "expected_items") and t.expected_items:
                    required = max(4, len(t.expected_items) * 2)
                    break

        if current_topic in self.minimum_required:
            required = self.minimum_required[current_topic]

        coverage = len(collected)

        return TopicGap(

            topic=current_topic,

            collected=collected,

            coverage=coverage,

            required=required,

            completed=(

                coverage >= required

            ),

        )