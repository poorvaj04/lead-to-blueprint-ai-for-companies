from src.agents.project_analyst_agent import ProjectAnalystAgent
from src.workflows.workflow_context import WorkflowContext
from src.engines.gap_analysis_engine import GapAnalysisEngine

class WebInterviewController:
    def __init__(self):
        self.agent = ProjectAnalystAgent()
        self.sessions = {}
        self.gap_engine = GapAnalysisEngine()

    def get_or_create_context(self, session_id: str, client_id: int, project_name: str) -> WorkflowContext:
        if session_id not in self.sessions:
            context = WorkflowContext()
            context.client_id = client_id
            context.project_name = project_name
            context.is_continuation = False
            
            # Check DB for hydration
            from src.database.session import SessionLocal
            from src.entities.project_qualification import ProjectQualification
            
            db = SessionLocal()
            try:
                qual = db.query(ProjectQualification).filter(
                    ProjectQualification.client_id == client_id,
                    ProjectQualification.project_name == project_name
                ).first()
                if qual and qual.requirements_json:
                    data = qual.requirements_json
                    from src.dtos.project_understanding import ProjectUnderstanding
                    from src.dtos.discovery_plan import DiscoveryPlan
                    from src.dtos.discovery_topic import DiscoveryTopic
                    from src.dtos.requirement_fact import RequirementFact
                    from src.dtos.conversation_message import ConversationMessage
                    
                    if data.get("project_understanding"):
                        context.project_understanding = ProjectUnderstanding(**data["project_understanding"])
                    if data.get("discovery_plan"):
                        context.discovery_plan = DiscoveryPlan(topics=[DiscoveryTopic(**t) for t in data["discovery_plan"]])
                    if data.get("requirement_facts"):
                        context.requirement_facts = [RequirementFact(**f) for f in data["requirement_facts"]]
                    if data.get("conversation_history"):
                        context.conversation_history = [ConversationMessage(**m) for m in data["conversation_history"]]
                        
                    context.is_continuation = True
                    context.final_decision = qual.final_decision
                    context.phase = "DISCOVERY" # Reset to discovery to allow continuing
            finally:
                db.close()
                
            self.sessions[session_id] = context
            
        return self.sessions[session_id]

    def process_message(self, client_message: str, session_id: str, client_id: int, project_name: str) -> dict:
        context = self.get_or_create_context(session_id, client_id, project_name)
        
        # Process through the agent
        result = self.agent.process_turn(context, client_message)
        
        # Format the modules roadmap for the UI
        modules_ui = []
        if context.discovery_plan:
            # First pass: map raw gaps
            for topic in context.discovery_plan.topics:
                gap = self.gap_engine.analyze(context, topic.name)
                modules_ui.append({
                    "name": topic.name,
                    "status": "completed" if (context.phase in ["CONFIRMATION", "COMPLETED"] or gap.completed) else "pending",
                    "coverage": gap.coverage,
                    "required": gap.required
                })
                
            # Second pass: enforce logical sequence (active module, past completed, future pending)
            active_index = -1
            if context.phase not in ["CONFIRMATION", "COMPLETED"]:
                for i, m in enumerate(modules_ui):
                    if m["status"] == "pending":
                        m["status"] = "active"
                        active_index = i
                        break
                        
            for i, m in enumerate(modules_ui):
                if context.phase in ["CONFIRMATION", "COMPLETED"]:
                    m["status"] = "completed"
                    m["percentage"] = 100
                else:
                    if active_index != -1 and i < active_index:
                        m["status"] = "completed"
                        m["percentage"] = 100
                    elif active_index != -1 and i > active_index:
                        m["status"] = "pending"
                        m["percentage"] = 0
                    elif i == active_index:
                        # Active topic: smooth progress calculation
                        # Guarantee at least 25% progress so it doesn't look stuck at 0
                        base_pct = 25
                        fact_pct = int((m["coverage"] / max(1, m["required"])) * 74)
                        m["percentage"] = min(99, base_pct + fact_pct)
                    else:
                        m["percentage"] = 100
        
        return {
            "response": result["response"],
            "modules": modules_ui,
            "completed": result.get("completed", False)
        }
