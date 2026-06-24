import json
from src.utils.logger import get_logger
from src.services.llm_service import LLMService
from src.dtos.risk_analysis import RiskAnalysis
from src.dtos.complexity_report import ComplexityReport
from src.dtos.feasibility_report import FeasibilityReport

class RiskAgent:
    def __init__(self):
        self.logger = get_logger("RiskAgent")
        self.llm = LLMService()

    def process(self, complexity: ComplexityReport, feasibility: FeasibilityReport) -> RiskAnalysis:
        self.logger.info("Goal: Assess the holistic risk of the project.")
        self.logger.info("Reason: Analyzing complexity and feasibility reports for potential pitfalls...")
        
        system_prompt = """You are a Corporate Risk Manager. 
Analyze the complexity and feasibility reports for a new software project.
Identify technical risks, business risks, and propose mitigation strategies.

CRITICAL RISK CALCULATION RULES:
1. The baseline Risk Score MUST be mathematically anchored to Complexity and Feasibility.
   - Low Complexity (<50) and High Feasibility (>70) = Baseline Risk of 10-30.
   - High Complexity (>70) and Low Feasibility (<50) = Baseline Risk of 70-90.
2. You may add a penalty (+10 to +20 points) if the project involves extreme Security or Regulatory requirements (e.g., HIPAA, medical data).
3. Final Risk Score must be between 0-100.
4. Determine the overall_risk_category based on your score: Low (0-30), Medium (31-60), High (61-80), or Critical (81-100).

Return JSON exactly matching this structure:
{
    "overall_risk_category": "string",
    "risk_score": int,
    "technical_risks": ["string"],
    "business_risks": ["string"],
    "mitigation_strategies": ["string"],
    "risk_reasoning": "string"
}"""
        
        user_prompt = f"Complexity Report:\n{json.dumps(complexity.model_dump())}\n\nFeasibility Report:\n{json.dumps(feasibility.model_dump())}"
        
        result = self.llm.generate_json(system_prompt, user_prompt)
        
        if not result["success"]:
            self.logger.error("Failed to generate risk analysis.")
            return RiskAnalysis(
                overall_risk_category="Unknown",
                risk_score=50,
                technical_risks=[],
                business_risks=[],
                mitigation_strategies=[],
                risk_reasoning="Failed to contact LLM."
            )
            
        content = result["content"]
        self.logger.info(f"Decision: Risk Score calculated as {content.get('risk_score')} ({content.get('overall_risk_category')})")
        self.logger.info("Action: Outputting RiskAnalysis JSON.")
        
        return RiskAnalysis(**content)
