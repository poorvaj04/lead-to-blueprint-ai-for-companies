from src.dtos.interview_decision import (
    InterviewDecision,
)

from src.services.prompt_manager import (
    PromptManager,
)

from src.services.llm_service import (
    LLMService,
)


class QuestionPlanningEngine:
    """
    Generates the next interview question
    using the LLM.
    """

    def __init__(self):

        self.prompt_manager = PromptManager()

        self.llm = LLMService()

    # ==================================================

    def generate(

        self,

        decision: InterviewDecision,

        workflow_context,

        current_topic: str,

    ) -> str:

        # ------------------------------------------

        if decision.question_style == "None":

            return ""

        # ------------------------------------------
        # Build prompts
        # ------------------------------------------

        system_prompt = self.prompt_manager.load_prompt(

            "question_generation_system"

        )

        project = workflow_context.project_understanding

        user_prompt = self.prompt_manager.load_prompt(

            "question_generation_user",

            project_type=project.project_type,

            business_domain=project.business_domain,

            business_problem=project.business_problem,

            current_topic=current_topic,

            objective=decision.objective,

            focus_area=decision.focus_area,

            reasoning=decision.reasoning,

            question_style=decision.question_style,

            conversation_history=workflow_context.get_conversation_text(),

        )

        # ------------------------------------------
        # Generate Question
        # ------------------------------------------

        result = self.llm.generate_text(

            system_prompt,

            user_prompt,

        )

        if result["success"]:

            return result["content"].strip()

        # ------------------------------------------
        # Fallback
        # ------------------------------------------

        return (

            "Could you tell me more about this?"

        )