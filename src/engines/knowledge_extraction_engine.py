from src.extractors.requirement_extractor import (
    RequirementExtractor,
)


class KnowledgeExtractionEngine:

    def __init__(self):

        self.extractor = RequirementExtractor()

    # ---------------------------------------------------------

    def update_knowledge(

        self,

        workflow_context,

        allowed_categories,

    ):

        if not workflow_context.conversation_history:

            return

        latest_message = (
            workflow_context.conversation_history[-1]
        )

        if latest_message.speaker != "Client":

            return

        # Build active modules text
        active_modules = ""
        if workflow_context.discovery_plan:
            for i, topic in enumerate(workflow_context.discovery_plan.topics):
                active_modules += f"Module {i+1}: {topic.name}\n"
                active_modules += f"Goal: {topic.goal}\n"
                if hasattr(topic, 'expected_items') and topic.expected_items:
                    active_modules += f"Targets: {', '.join(topic.expected_items)}\n"
                active_modules += "\n"

        facts = self.extractor.extract(

            active_modules=active_modules,

            allowed_categories=allowed_categories,

            client_answer=latest_message.message,

        )

        self._add_new_facts(

            workflow_context,

            facts,

        )

    # ---------------------------------------------------------

    def _add_new_facts(

        self,

        workflow_context,

        new_facts,

    ):

        for fact in new_facts:

            duplicate = False

            for existing in workflow_context.requirement_facts:

                if (

                    existing.topic == fact.topic

                    and existing.category == fact.category

                    and existing.key.lower() == fact.key.lower()

                ):

                    duplicate = True

                    break

            if not duplicate:

                workflow_context.requirement_facts.append(
                    fact
                )