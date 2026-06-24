from pydantic import BaseModel, Field
from typing import Optional, List
from src.dtos.complexity_report import ComplexityReport
from src.dtos.feasibility_report import FeasibilityReport
from src.dtos.risk_analysis import RiskAnalysis

class CRMReport(BaseModel):
    project_name: str
    client_id: int
    qualification_id: int
    complexity_report: ComplexityReport
    feasibility_report: FeasibilityReport
    # Resource gaps
    missing_roles: List[str] = Field(default_factory=list)
    missing_infrastructure: List[str] = Field(default_factory=list)
    partially_available_roles: List[str] = Field(default_factory=list)
    missing_technologies: List[str]
    
    risk_analysis: RiskAnalysis
    final_decision: str
    decision_reasoning: str
