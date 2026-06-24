import json
import re


class JsonParser:

    @staticmethod
    def parse(text: str):

        if not isinstance(text, str):
            return text

        text = text.strip()

        text = text.strip()

        # ------------------------------------
        # Extract substring between { and }
        # ------------------------------------
        start_idx = text.find('{')
        end_idx = text.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            text = text[start_idx:end_idx+1]
        
        text = text.strip()

        # ------------------------------------
        # Repair Common LLM Mistakes
        # ------------------------------------

        # ""name"  ->  "name"
        text = re.sub(
            r'""([A-Za-z0-9_]+)"',
            r'"\1"',
            text,
        )

        # Remove trailing commas

        text = re.sub(
            r",(\s*[}\]])",
            r"\1",
            text,
        )

        # ------------------------------------
        # Parse
        # ------------------------------------

        return json.loads(text)