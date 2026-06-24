from pydantic import BaseModel, Field
from typing import List

class FeasibilityReport(BaseModel):
    is_feasible: bool
    feasibility_score: int
    technical_feasibility_score: int
    resource_availability_score: int
    budget_timeline_feasibility_score: int
    regulatory_and_legal_constraints: str
    historical_project_match: str
    third_party_vendor_risks: str
    missing_technologies: List[str] = Field(default_factory=list)
    missing_roles: List[str] = Field(default_factory=list)
    missing_infrastructure: List[str] = Field(default_factory=list)
    partially_available_roles: List[str] = Field(default_factory=list)
    feasibility_reasoning: str
