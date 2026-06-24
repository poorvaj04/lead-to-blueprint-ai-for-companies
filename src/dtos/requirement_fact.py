from dataclasses import dataclass


@dataclass
class RequirementFact:

    topic: str

    category: str

    key: str

    value: str

    source: str = "Client"

    confidence: int = 100

    verified: bool = False