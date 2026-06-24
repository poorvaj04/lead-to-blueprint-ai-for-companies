from src.dtos.requirement_fact import (
    RequirementFact,
)
from src.services.llm_service import (
    LLMService,
)
from src.services.prompt_manager import (
    PromptManager,
)


class RequirementExtractor:

    def __init__(self):

        self.prompt_manager = PromptManager()

        self.llm = LLMService()

    # ---------------------------------------------------------

    def extract(

        self,

        active_modules: str,

        allowed_categories: list[str],

        client_answer: str,

    ) -> list[RequirementFact]:

        system_prompt = self.prompt_manager.load_prompt(
            "requirement_extractor/system"
        )

        user_prompt = self.prompt_manager.load_prompt(

            "requirement_extractor/user",

            active_modules=active_modules,

            allowed_categories="\n".join(
                allowed_categories
            ),

            client_answer=client_answer,

        )

        result = self.llm.generate(
            system_prompt,
            user_prompt,
        )

        if not result["success"]:

            return []

        content = result["content"]

        facts = []

        for item in content.get(

            "facts",

            [],

        ):

            facts.append(

                RequirementFact(

                    topic=item.get(
                        "topic",
                        "General",
                    ),

                    category=item.get(
                        "category",
                        "",
                    ),

                    key=item.get(
                        "key",
                        "",
                    ),

                    value=item.get(
                        "value",
                        "",
                    ),

                    confidence=item.get(
                        "confidence",
                        100,
                    ),

                )

            )

        return facts