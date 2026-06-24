from dataclasses import dataclass


@dataclass
class ProjectUnderstanding:

    # ----------------------------------
    # Business Understanding
    # ----------------------------------

    business_problem: str = ""

    desired_business_outcome: str = ""

    assumptions: list[str] | None = None

    # ----------------------------------
    # Project Understanding
    # ----------------------------------

    project_type: str = ""

    business_domain: str = ""

    project_intent: str = ""

    project_nature: str = ""

    complexity: str = ""

    # ----------------------------------
    # AI Internal
    # ----------------------------------

    planner_reasoning: str = ""

    discovery_strategy: str = ""

    # ----------------------------------
    # Summary
    # ----------------------------------

    summary: str = ""

    def __post_init__(self):

        if self.assumptions is None:

            self.assumptions = []