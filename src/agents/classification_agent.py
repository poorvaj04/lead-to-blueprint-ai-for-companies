import json
from src.utils.logger import get_logger
from src.services.llm_service import LLMService
from src.dtos.risk_analysis import RiskAnalysis
from src.dtos.complexity_report import ComplexityReport
from src.dtos.feasibility_report import FeasibilityReport

class ClassificationAgent:
    def __init__(self):
        self.logger = get_logger("ClassificationAgent")
        self.llm = LLMService()

    def process(self, risk: RiskAnalysis, complexity: ComplexityReport, feasibility: FeasibilityReport) -> tuple[str, str]:
        self.logger.info("Goal: Classify the final corporate decision for this project.")
        self.logger.info("Reason: Weighing feasibility, complexity, and risk factors...")
        
        system_prompt = """You are the VP of Engineering. Make the final call on whether the company should accept this software project.
You must output exactly one of these decisions: "Approved" or "Rejected".
Rule: If feasibility is < 60 or Risk is High or Critical, you must reject it. Otherwise, approve it.

Return JSON exactly matching this structure:
{
    "final_decision": "string",
    "decision_reasoning": "string"
}"""
        
        user_prompt = f"Complexity: {json.dumps(complexity.model_dump())}\nFeasibility: {json.dumps(feasibility.model_dump())}\nRisk: {json.dumps(risk.model_dump())}"
        
        result = self.llm.generate_json(system_prompt, user_prompt)
        
        if not result["success"]:
            self.logger.error("Failed to generate classification.")
            return "Rejected", "Fallback decision due to API failure."
            
        content = result["content"]
        decision = content.get("final_decision", "Rejected")
        reasoning = content.get("decision_reasoning", "No reasoning provided.")
        
        self.logger.info(f"Decision: Final decision is {decision}")
        self.logger.info("Action: Passing decision to the next phase.")
        
        return decision, reasoning
