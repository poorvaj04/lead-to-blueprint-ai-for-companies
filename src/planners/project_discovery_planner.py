import json

from src.dtos.discovery_plan import (
    DiscoveryPlan,
)
from src.dtos.discovery_topic import (
    DiscoveryTopic,
)
from src.dtos.project_understanding import (
    ProjectUnderstanding,
)
from src.services.llm_service import (
    LLMService,
)
from src.services.prompt_manager import (
    PromptManager,
)


class ProjectDiscoveryPlanner:

    def __init__(self):

        self.prompt_manager = PromptManager()

        self.llm = LLMService()

    # --------------------------------------------------

    def plan(
        self,
        first_client_request: str,
    ):

        system_prompt = self.prompt_manager.load_prompt(
            "project_discovery/system"
        )

        user_prompt = self.prompt_manager.load_prompt(
            "project_discovery/user",
            first_client_request=first_client_request,
        )

        result = self.llm.generate(
            system_prompt,
            user_prompt,
        )

        if not result["success"]:
            raise RuntimeError(result["error"])

        content = result["content"]

        project = content["project_understanding"]

        understanding = ProjectUnderstanding(

            business_problem=project.get(
                "business_problem",
                "",
            ),

            desired_business_outcome=project.get(
                "desired_business_outcome",
                "",
            ),

            assumptions=project.get(
                "assumptions",
                [],
            ),

            project_type=project.get(
                "project_type",
                "",
            ),

            business_domain=project.get(
                "business_domain",
                "",
            ),

            project_intent=project.get(
                "project_intent",
                "",
            ),

            project_nature=project.get(
                "project_nature",
                "",
            ),

            complexity=project.get(
                "complexity",
                "",
            ),

            planner_reasoning=project.get(
                "planner_reasoning",
                "",
            ),

            discovery_strategy=project.get(
                "discovery_strategy",
                "",
            ),

            summary=project.get(
                "summary",
                "",
            ),
        )

        plan = content["discovery_plan"]

        discovery_plan = DiscoveryPlan(

            project_title=plan.get(
                "project_title",
                "",
            ),

            overall_goal=plan.get(
                "overall_goal",
                "",
            ),
        )

        for topic in plan.get(
            "topics",
            [],
        ):

            discovery_plan.topics.append(

                DiscoveryTopic(

                    name=topic.get(
                        "name",
                        "",
                    ),

                    goal=topic.get(
                        "goal",
                        "",
                    ),

                    expected_items=topic.get(
                        "expected_items",
                        [],
                    ),
                )

            )

        return understanding, discovery_plan