import re


class TextNormalizationService:
    """
    Cleans Whisper transcript before sending it
    to the AI agents.
    """

    def __init__(self):

        self.filler_words = {

            "uh",
            "um",
            "hmm",
            "ah",
            "er",
            "okay",
            "ok",
            "actually",
            "basically",

        }

    # --------------------------------------------------

    def _remove_fillers(
        self,
        text: str
    ) -> str:

        words = []

        for word in text.split():

            cleaned = word.lower().strip(".,!?")

            if cleaned not in self.filler_words:

                words.append(word)

        return " ".join(words)

    # --------------------------------------------------

    def _remove_extra_spaces(
        self,
        text: str
    ) -> str:

        return re.sub(
            r"\s+",
            " ",
            text
        ).strip()

    # --------------------------------------------------

    def _remove_repeated_words(
        self,
        text: str
    ) -> str:

        words = text.split()

        if not words:
            return text

        cleaned = [words[0]]

        previous = re.sub(
            r"[^\w]",
            "",
            words[0].lower()
        )

        for word in words[1:]:

            current = re.sub(
                r"[^\w]",
                "",
                word.lower()
            )

            if current != previous:

                cleaned.append(word)

                previous = current

        return " ".join(cleaned)

    # --------------------------------------------------

    def _capitalize(
        self,
        text: str
    ) -> str:

        if not text:

            return text

        text = text[0].upper() + text[1:]

        if text[-1] not in ".!?":

            text += "."

        return text

    # --------------------------------------------------

    def normalize(
        self,
        text: str
    ) -> str:

        text = self._remove_fillers(text)

        text = self._remove_extra_spaces(text)

        text = self._remove_repeated_words(text)

        text = self._capitalize(text)

        return text