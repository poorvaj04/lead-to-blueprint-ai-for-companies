from pathlib import Path

from src.config.settings import settings


class PromptManager:
    """
    Loads prompt templates and replaces variables.
    """

    def __init__(self):

        self.prompt_directory = settings.PROMPT_DIR

    # --------------------------------------------------

    def load_prompt(
        self,
        prompt_name: str,
        **kwargs,
    ) -> str:

        prompt_file = (
            self.prompt_directory /
            f"{prompt_name}.txt"
        )

        if not prompt_file.exists():

            raise FileNotFoundError(

                f"Prompt not found : {prompt_file}"

            )

        prompt = prompt_file.read_text(
            encoding="utf-8"
        )

        for key, value in kwargs.items():

            placeholder = f"{{{key}}}"

            prompt = prompt.replace(

                placeholder,

                str(value)

            )

        return prompt