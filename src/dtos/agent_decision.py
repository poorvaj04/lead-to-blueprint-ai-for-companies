from dataclasses import dataclass


@dataclass
class AgentDecision:

    decision: str

    reason: str

    next_question: str

    confidence: int