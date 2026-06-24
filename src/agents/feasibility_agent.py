import json
from src.utils.logger import get_logger
from src.services.llm_service import LLMService
from src.dtos.feasibility_report import FeasibilityReport
from src.dtos.complexity_report import ComplexityReport
from src.database.session import SessionLocal
from src.entities.technology import Technology
from src.entities.skill import Skill
from src.entities.employee import Employee
from src.entities.employee_skill import EmployeeSkill
from src.entities.employee_availability import EmployeeAvailability
from src.entities.completed_project import CompletedProject

class FeasibilityAgent:
    """
    Evaluates project feasibility by cross-referencing Complexity Agent outputs
    with the Company Knowledge Base (DB) and using LLM for regulatory/market analysis.
    """

    def __init__(self):
        self.logger = get_logger("FeasibilityAgent")
        self.llm = LLMService()

    def process(self, requirements_json: dict, complexity_report: ComplexityReport) -> FeasibilityReport:
        self.logger.info("Goal: Perform a strict corporate-level viability assessment.")
        self.logger.info("Reason: Querying Company Knowledge Base to match skills, availability, and tech stack...")
        
        db = SessionLocal()
        
        try:
            # 1. Fetch available company resources from Database
            company_tech = db.query(Technology).all()
            company_tech_list = [f"{t.technology_name} ({t.technology_category})" for t in company_tech]
            
            from src.entities.infrastructure import Infrastructure
            company_infra = db.query(Infrastructure).filter(Infrastructure.availability_status == "Available").all()
            company_infra_list = [f"{i.infrastructure_category}: {i.resource_name} ({i.resource_type}, Qty: {i.quantity})" for i in company_infra]
            
            # Fetch all unique skills and roles from employees who are available
            company_skills_list = []
            company_roles_list = []
            available_employees = db.query(EmployeeAvailability).filter(
                EmployeeAvailability.availability_status.in_(["Available", "Partially Available"]),
                EmployeeAvailability.available_hours_per_week >= 10
            ).all()
            
            for avail in available_employees:
                emp = db.query(Employee).filter(Employee.employee_id == avail.employee_id).first()
                if emp and emp.designation not in company_roles_list:
                    company_roles_list.append(emp.designation)
                
                emp_skills = db.query(EmployeeSkill).filter(EmployeeSkill.employee_id == avail.employee_id).all()
                for es in emp_skills:
                    skill = db.query(Skill).filter(Skill.skill_id == es.skill_id).first()
                    if skill and skill.skill_name not in company_skills_list:
                        company_skills_list.append(skill.skill_name)
            
            # 2. Historical Post-Mortem
            historical_match_text = "No direct historical match found."
            if complexity_report.recommended_technologies:
                past_proj = db.query(CompletedProject).first()
                if past_proj:
                    status_name = past_proj.project_status.name if hasattr(past_proj.project_status, 'name') else str(past_proj.project_status)
                    historical_match_text = f"Found past project '{past_proj.project_name}' ({status_name}). Duration: {past_proj.duration_months} months."
            
            # 3. Use LLM for Semantic Matching and Constraint Analysis
            system_prompt = """You are a Corporate Feasibility Analyst. 
Your job is to cross-reference the project's recommended technologies and required roles against the company's ACTUAL available tech stack, available employee roles, and skills.

IMPORTANT RULES FOR MATCHING:
- Perform SEMANTIC matching. If the project requires "Cloud-based infrastructure" and the company has "AWS", that is a MATCH. Do NOT list it as missing.
- If the project requires "Relational databases" and the company has "PostgreSQL", that is a MATCH. Do NOT list it as missing.
- Check BOTH the 'Available Employee Roles' and 'Available Employee Skills'. If the required role is semantically covered by either list, it is a MATCH. Do NOT list it as missing.
- Check 'Company Infrastructure'. If the project requires specific servers, cloud compute, or networking, cross-reference it.
- Only list items in `missing_technologies`, `missing_roles`, or `missing_infrastructure` if the company truly lacks the capability.

Also, analyze the requirements for Regulatory constraints (e.g., HIPAA) and Third-Party Vendor Risks.

Return a JSON exactly matching this structure:
{
    "missing_technologies": ["List of tech NOT covered by company tech"],
    "missing_roles": ["List of roles NOT covered by company skills"],
    "missing_infrastructure": ["List of infrastructure NOT covered by company infrastructure"],
    "technical_feasibility_score": int (0-100, deduct 15 points per missing tech),
    "resource_availability_score": int (0-100, deduct 20 points per missing role),
    "budget_timeline_feasibility_score": int (0-100 score on if the timeline seems realistic),
    "regulatory_and_legal_constraints": "string",
    "third_party_vendor_risks": "string",
    "feasibility_reasoning": "string"
}"""
            
            user_prompt = f"""Project Requirements:
{json.dumps(requirements_json)}

Complexity Report Required Tech: {complexity_report.recommended_technologies}
Complexity Report Required Roles: {complexity_report.required_roles}
Complexity Duration: {complexity_report.estimated_duration_months} months.

=== COMPANY RESOURCES (USE THESE FOR MATCHING) ===
Company Tech Stack: {company_tech_list}
Company Infrastructure: {company_infra_list}
Available Employee Roles (Job Titles): {company_roles_list}
Available Employee Skills: {company_skills_list}"""
            
            llm_result = self.llm.generate_json(system_prompt, user_prompt)
            
            if llm_result["success"]:
                llm_data = llm_result["content"]
            else:
                llm_data = {
                    "missing_technologies": complexity_report.recommended_technologies,
                    "missing_roles": complexity_report.required_roles,
                    "missing_infrastructure": [],
                    "technical_feasibility_score": 0,
                    "resource_availability_score": 0,
                    "regulatory_and_legal_constraints": "Unknown",
                    "third_party_vendor_risks": "Unknown",
                    "budget_timeline_feasibility_score": 50,
                    "feasibility_reasoning": "Failed to analyze feasibility due to LLM error."
                }
            
            missing_roles = llm_data.get("missing_roles", [])
            missing_infra = llm_data.get("missing_infrastructure", [])
            technical_feasibility_score = llm_data.get("technical_feasibility_score", 0)
            resource_availability_score = llm_data.get("resource_availability_score", 0)
            
            # Penalize overall score by 8 points per missing infrastructure item
            infra_penalty = len(missing_infra) * 8
            
            # Calculate overall feasibility
            overall_score = (technical_feasibility_score + resource_availability_score + llm_data.get("budget_timeline_feasibility_score", 50)) // 3
            overall_score = max(0, overall_score - infra_penalty)
            
            is_feasible = overall_score >= 60 and len(missing_roles) <= 2
            
            # Python-only extraction of partially available roles
            partially_available_roles_info = []
            for avail in available_employees:
                if avail.availability_status == "Partially Available":
                    emp = db.query(Employee).filter(Employee.employee_id == avail.employee_id).first()
                    if emp:
                        partially_available_roles_info.append(f"{emp.designation} - Partially Available ({avail.available_hours_per_week} hours/week)")
            
            self.logger.info(f"Decision: Feasibility Score: {overall_score}, Is Feasible: {is_feasible}")
            self.logger.info("Action: Outputting FeasibilityReport JSON.")
            
            return FeasibilityReport(
                is_feasible=is_feasible,
                feasibility_score=overall_score,
                technical_feasibility_score=technical_feasibility_score,
                resource_availability_score=resource_availability_score,
                budget_timeline_feasibility_score=llm_data.get("budget_timeline_feasibility_score", 50),
                regulatory_and_legal_constraints=llm_data.get("regulatory_and_legal_constraints", "None"),
                historical_project_match=historical_match_text,
                third_party_vendor_risks=llm_data.get("third_party_vendor_risks", "None"),
                missing_technologies=llm_data.get("missing_technologies", []),
                missing_roles=missing_roles,
                missing_infrastructure=missing_infra,
                partially_available_roles=partially_available_roles_info,
                feasibility_reasoning=llm_data.get("feasibility_reasoning", "Analyzed successfully.")
            )
            
        finally:
            db.close()
