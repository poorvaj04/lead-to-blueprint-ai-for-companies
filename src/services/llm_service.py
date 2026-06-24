import time
from groq import Groq
from src.config.settings import settings
from src.utils.logger import get_logger
from src.parsers.json_parser import JsonParser


class LLMService:
    """
    Central service for communicating with the LLM.
    """

    def __init__(self):
        self.logger = get_logger("LLMService")
        
        self.api_keys = settings.GROQ_API_KEYS
        if not self.api_keys:
            self.logger.error("No GROQ_API_KEYS are set in environment!")
            
        self.models = [settings.GROQ_MODEL, settings.GROQ_FALLBACK_MODEL]

    # ==================================================
    # Internal Chat
    # ==================================================

    def _chat(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:
        start = time.perf_counter()
        
        last_error = None
        for api_key in self.api_keys:
            client = Groq(api_key=api_key)
            for model in self.models:
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        temperature=0,
                        response_format={"type": "json_object"} if "valid json" in system_prompt.lower() else None
                    )
                    
                    latency = time.perf_counter() - start
                    raw_content = response.choices[0].message.content.strip()

                    return {
                        "success": True,
                        "raw_content": raw_content,
                        "latency": latency,
                        "model": model,
                    }
                except Exception as error:
                    last_error = str(error)
                    self.logger.warning(f"Key {api_key[:8]}... with model {model} failed. Error: {last_error}")

        # If we exhausted all combinations
        latency = time.perf_counter() - start
        self.logger.error(f"All API keys and models exhausted. Last error: {last_error}")
        return {
            "success": False,
            "raw_content": None,
            "error": last_error,
            "latency": latency,
            "model": "All Failed",
        }

    # ==================================================
    # JSON Response
    # ==================================================

    def generate_json(

        self,

        system_prompt: str,

        user_prompt: str,

    ) -> dict:

        result = self._chat(

            system_prompt,

            user_prompt,

        )

        if not result["success"]:

            return {

                "success": False,

                "content": None,

                "error": result["error"],

                "latency": result["latency"],

                "model": result["model"],

            }

        content = JsonParser.parse(

            result["raw_content"]

        )

        return {

            "success": True,

            "content": content,

            "latency": result["latency"],

            "model": result["model"],

        }

    # ==================================================
    # Plain Text Response
    # ==================================================

    def generate_text(

        self,

        system_prompt: str,

        user_prompt: str,

    ) -> dict:

        result = self._chat(

            system_prompt,

            user_prompt,

        )

        if not result["success"]:

            return {

                "success": False,

                "content": None,

                "error": result["error"],

                "latency": result["latency"],

                "model": result["model"],

            }

        return {

            "success": True,

            "content": result["raw_content"],

            "latency": result["latency"],

            "model": result["model"],

        }

    # ==================================================
    # Backward Compatibility
    # ==================================================

    def generate(

        self,

        system_prompt: str,

        user_prompt: str,

    ) -> dict:

        return self.generate_json(

            system_prompt,

            user_prompt,

        )