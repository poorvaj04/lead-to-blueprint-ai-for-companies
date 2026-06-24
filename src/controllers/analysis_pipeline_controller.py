from src.database.session import SessionLocal
from src.entities.project_qualification import ProjectQualification
from src.agents.complexity_agent import ComplexityAgent
from src.agents.feasibility_agent import FeasibilityAgent
from src.agents.risk_agent import RiskAgent
from src.agents.classification_agent import ClassificationAgent
from src.agents.crm_agent import CRMAgent
from src.agents.notification_agent import NotificationAgent
from src.utils.logger import get_logger

class AnalysisPipelineController:
    """
    Orchestrates the background execution of the Complexity and Feasibility agents 
    after the initial client interview completes.
    """
    
    def __init__(self):
        self.logger = get_logger("AnalysisPipeline")
        self.complexity_agent = ComplexityAgent()
        self.feasibility_agent = FeasibilityAgent()
        self.risk_agent = RiskAgent()
        self.classification_agent = ClassificationAgent()
        self.crm_agent = CRMAgent()
        self.notification_agent = NotificationAgent()
        
    def run_pipeline(self, client_id: int, project_name: str):
        self.logger.info(f"Starting Phase 2 Pipeline for Project: '{project_name}'")
        
        db = SessionLocal()
        try:
            # 1. Fetch qualification record
            qual = db.query(ProjectQualification).filter(
                ProjectQualification.client_id == client_id,
                ProjectQualification.project_name == project_name
            ).first()
            
            if not qual or not qual.requirements_json:
                self.logger.error("Qualification record or requirements JSON not found. Aborting.")
                return
                
            requirements_json = qual.requirements_json
            
            # Compress requirements to prevent LLM Token Overflow
            compressed_requirements = {
                "project_understanding": requirements_json.get("project_understanding", {}),
                "requirement_facts": requirements_json.get("requirement_facts", [])
            }
            
            # 2. Run Complexity Agent
            self.logger.info("=== Executing Complexity Agent ===")
            complexity_report = self.complexity_agent.process(compressed_requirements)
            
            qual.complexity_score = complexity_report.complexity_score
            qual.complexity_report = complexity_report.model_dump()
            db.commit()
            
            # 3. Run Feasibility Agent
            self.logger.info("=== Executing Feasibility Agent ===")
            feasibility_report = self.feasibility_agent.process(compressed_requirements, complexity_report)
            
            qual.feasibility_report = feasibility_report.model_dump()
            db.commit()
            
            # 4. Run Risk Agent
            self.logger.info("=== Executing Risk Agent ===")
            risk_report = self.risk_agent.process(complexity_report, feasibility_report)
            
            qual.risk_analysis = risk_report.model_dump()
            db.commit()
            
            # 5. Run Classification Agent
            self.logger.info("=== Executing Classification Agent ===")
            final_decision, decision_reasoning = self.classification_agent.process(risk_report, complexity_report, feasibility_report)
            
            qual.final_decision = final_decision
            db.commit()
            
            # 6. Run CRM Agent
            self.logger.info("=== Executing CRM Agent ===")
            crm_report = self.crm_agent.process(
                project_name=qual.project_name,
                client_id=qual.client_id,
                qualification_id=qual.qualification_id,
                complexity=complexity_report,
                feasibility=feasibility_report,
                risk=risk_report,
                final_decision=final_decision,
                decision_reasoning=decision_reasoning
            )
            
            # 7. Run Notification Agent
            self.logger.info("=== Executing Notification Agent ===")
            self.notification_agent.process(crm_report)
            
            self.logger.info(f"Phase 3 Pipeline Complete for '{project_name}'")
            
        except Exception as e:
            self.logger.error(f"Pipeline error: {str(e)}")
            db.rollback()
        finally:
            db.close()
