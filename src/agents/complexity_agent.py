import json
from src.utils.logger import get_logger
from src.services.llm_service import LLMService
from src.dtos.complexity_report import ComplexityReport
from src.database.session import SessionLocal
from src.entities.employee import Employee

class ComplexityAgent:
    """
    Analyzes project requirements to estimate technical complexity, 
    security risks, required roles, and tech stack.
    """

    def __init__(self):
        self.logger = get_logger("ComplexityAgent")
        self.llm = LLMService()

    def process(self, requirements_json: dict) -> ComplexityReport:
        self.logger.info("Goal: Perform an enterprise-grade technical analysis of the project's difficulty.")
        self.logger.info("Reason: Analyzing facts to deduce security risks, data processing demands, and architectural burden...")
        db = SessionLocal()
        try:
            employee_count = db.query(Employee).count()
        finally:
            db.close()
            
        system_prompt = """You are an Enterprise Technical Architect.
Your task is to analyze the provided project requirements and estimate the technical complexity.

CRITICAL: You must consider the Company Size when calculating the Complexity Score. 
A highly complex project might score 85/100 for a 2-person company, but the exact same project might only score 40/100 for a 20-person company because the workload can be distributed and parallelized. Adjust your score based on the provided Company Size.

You must evaluate:
1. Security Risk Level (Low/Medium/High/Critical): e.g. handles payments or PII = High/Critical.
2. Architecture Complexity: Evaluate integrations, third-party APIs, and system scale.
3. Data Processing Demands: Estimate TPS and data volume.
4. Recommended Technologies: What tech stack is ideal for this?
5. Required Roles: What roles are needed (e.g., Frontend Developer, Cloud Architect, QA)?
6. Estimated Duration Months: How many months to build?
7. Complexity Score: 0-100 score. SCALED INVERSELY based on the company size.

Return valid JSON exactly matching this structure:
{
    "complexity_score": int,
    "architecture_complexity": "string",
    "security_risk_level": "string",
    "data_processing_demands": "string",
    "integration_dependencies": "string",
    "recommended_technologies": ["tech1", "tech2"],
    "required_roles": ["role1", "role2"],
    "estimated_duration_months": int,
    "complexity_reasoning": "string"
}"""
        
        user_prompt = f"Company Size: {employee_count} employees.\n\nProject Requirements:\n{json.dumps(requirements_json, indent=2)}\n\nGenerate the Complexity Report JSON, adjusting the score based on the company size."
        
        result = self.llm.generate_json(system_prompt, user_prompt)
        
        if not result["success"]:
            self.logger.error(f"Failed to generate complexity report: {result.get('error')}")
            # Fallback
            return ComplexityReport(
                complexity_score=50,
                architecture_complexity="Unknown",
                security_risk_level="Unknown",
                data_processing_demands="Unknown",
                integration_dependencies="Unknown",
                recommended_technologies=[],
                required_roles=[],
                estimated_duration_months=0,
                complexity_reasoning="Failed to generate report"
            )
            
        content = result["content"]
        
        import random
        base_score = content.get("complexity_score", 50)
        # Add a small natural variance so the score isn't perfectly constant on every run
        variance = random.randint(-4, 4)
        final_score = max(0, min(100, base_score + variance))
        content["complexity_score"] = final_score
        
        self.logger.info(f"Decision: Calculated Complexity Score: {final_score}")
        self.logger.info("Action: Outputting ComplexityReport JSON.")
        
        return ComplexityReport(**content)
