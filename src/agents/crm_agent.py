from src.utils.logger import get_logger
from src.dtos.crm_report import CRMReport
from src.dtos.risk_analysis import RiskAnalysis
from src.dtos.complexity_report import ComplexityReport
from src.dtos.feasibility_report import FeasibilityReport

class CRMAgent:
    def __init__(self):
        self.logger = get_logger("CRMAgent")

    def process(self, project_name: str, client_id: int, qualification_id: int, 
                complexity: ComplexityReport, feasibility: FeasibilityReport, 
                risk: RiskAnalysis, final_decision: str, decision_reasoning: str) -> CRMReport:
        self.logger.info("Goal: Package the analysis data into a structured CRM format.")
        self.logger.info("Reason: The data needs to be uniformly modeled for the Manager Notification portal.")
        
        report = CRMReport(
            project_name=project_name,
            client_id=client_id,
            qualification_id=qualification_id,
            complexity_report=complexity,
            feasibility_report=feasibility,
            missing_roles=feasibility.missing_roles,
            missing_technologies=feasibility.missing_technologies,
            missing_infrastructure=feasibility.missing_infrastructure,
            partially_available_roles=feasibility.partially_available_roles,
            risk_analysis=risk,
            final_decision=final_decision,
            decision_reasoning=decision_reasoning
        )
        
        self.logger.info("Decision: Structured CRM Report created.")
        self.logger.info("Action: Outputting CRMReport DTO.")
        return report
