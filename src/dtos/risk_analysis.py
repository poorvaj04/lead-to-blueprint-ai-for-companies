from pydantic import BaseModel
from typing import List

class RiskAnalysis(BaseModel):
    overall_risk_category: str
    risk_score: int
    technical_risks: List[str]
    business_risks: List[str]
    mitigation_strategies: List[str]
    risk_reasoning: str
