from src.dtos.interview_decision import (
    InterviewDecision,
)


class InterviewReasoner:
    """
    Decides what the interviewer should
    focus on next.
    """

    # ==================================================

    def reason(

        self,

        workflow_context,

        topic_gap,

    ) -> InterviewDecision:

        topic = topic_gap.topic

        # Future AI-03 reasoning inputs
        project = workflow_context.project_understanding
        conversation = workflow_context.conversation_history
        facts = workflow_context.requirement_facts

        _ = project
        _ = conversation
        _ = facts

        # =================================================
        # Core Features
        # =================================================

        if topic == "Core Features":

            if topic_gap.coverage == 0:

                return InterviewDecision(

                    interview_strategy="Discovery",

                    objective="Understand Core Features",

                    focus_area="General Features",

                    reasoning=(
                        "No software features have been "
                        "discussed yet."
                    ),

                    question_style="Open",

                    priority="High",

                    confidence=95,

                )

            if topic_gap.completed:

                return InterviewDecision(

                    interview_strategy="Completion",

                    objective="Core Features Completed",

                    focus_area="None",

                    reasoning=(
                        "Enough feature information "
                        "has been collected."
                    ),

                    question_style="None",

                    priority="None",

                    confidence=100,

                )

            return InterviewDecision(

                interview_strategy="Investigation",

                objective="Understand Core Features",

                focus_area="Missing Features",

                reasoning=(
                    "Some software features have "
                    "already been collected, but "
                    "additional functionality is "
                    "still required."
                ),

                question_style="Focused",

                priority="High",

                confidence=90,

            )

        # =================================================
        # Business Goals
        # =================================================

        if topic == "Business Goals":

            return InterviewDecision(

                interview_strategy="Discovery",

                objective="Understand Business Goals",

                focus_area="Business Objectives",

                reasoning=(
                    "Business goals should be clarified "
                    "before moving to detailed requirements."
                ),

                question_style="Open",

                priority="High",

                confidence=90,

            )

        # =================================================
        # Current Process
        # =================================================

        if topic == "Current Process":

            return InterviewDecision(

                interview_strategy="Investigation",

                objective="Understand Current Process",

                focus_area="Existing Workflow",

                reasoning=(
                    "Current workflow information "
                    "is needed to understand the client's "
                    "operations."
                ),

                question_style="Exploration",

                priority="Medium",

                confidence=90,

            )

        # =================================================
        # Integration Needs
        # =================================================

        if topic == "Integration Needs":

            return InterviewDecision(

                interview_strategy="Discovery",

                objective="Understand Integrations",

                focus_area="External Systems",

                reasoning=(
                    "Identify software and services "
                    "that must connect with the solution."
                ),

                question_style="Focused",

                priority="Medium",

                confidence=90,

            )

        # =================================================
        # Default
        # =================================================

        return InterviewDecision(

            interview_strategy="Discovery",

            objective="Continue Discovery",

            focus_area="General",

            reasoning="Continue requirement discovery.",

            question_style="Open",

            priority="Medium",

            confidence=80,

        )