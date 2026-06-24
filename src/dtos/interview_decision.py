from dataclasses import dataclass


@dataclass
class InterviewDecision:
    """
    Decision produced by the Interview Reasoner.
    """

    # Overall interview strategy
    interview_strategy: str

    # Current discovery objective
    objective: str

    # Specific area to investigate
    focus_area: str

    # Why this decision was made
    reasoning: str

    # How the question should be asked
    question_style: str

    # Priority of this investigation
    priority: str

    # Confidence in this decision
    confidence: int