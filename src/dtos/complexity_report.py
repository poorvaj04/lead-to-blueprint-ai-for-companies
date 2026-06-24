from pydantic import BaseModel
from typing import List

class ComplexityReport(BaseModel):
    complexity_score: int
    architecture_complexity: str
    security_risk_level: str
    data_processing_demands: str
    integration_dependencies: str
    recommended_technologies: List[str]
    required_roles: List[str]
    estimated_duration_months: int
    complexity_reasoning: str
