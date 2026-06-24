from src.utils.logger import get_logger
from src.workflows.workflow_context import WorkflowContext
from src.planners.project_discovery_planner import ProjectDiscoveryPlanner
from src.engines.gap_analysis_engine import GapAnalysisEngine
from src.engines.interview_reasoner import InterviewReasoner
from src.engines.question_planning_engine import QuestionPlanningEngine
from src.engines.knowledge_extraction_engine import KnowledgeExtractionEngine
from src.dtos.conversation_message import ConversationMessage

class ProjectAnalystAgent:
    def __init__(self):
        self.logger = get_logger("Project Analyst Agent")
        self.planner = ProjectDiscoveryPlanner()
        self.gap_engine = GapAnalysisEngine()
        self.reasoner = InterviewReasoner()
        self.question_engine = QuestionPlanningEngine()
        self.knowledge_engine = KnowledgeExtractionEngine()
        
        # Categories we care about for knowledge extraction
        self.allowed_categories = [
            "Feature", "Module", "Integration", "Automation",
            "Business Problem", "Pain Point", "Desired Outcome",
            "Business Objective", "Existing System", "Workflow",
            "Manual Process", "Bottleneck", "Timeline", "Budget", "Priority"
        ]

    def process_turn(self, workflow_context: WorkflowContext, client_message: str) -> dict:
        self.logger.info(f"[CLIENT] {client_message}")
        
        # Add client message to history
        workflow_context.add_client_message(client_message)

        if workflow_context.phase == "COMPLETED":
            return {"response": "The project requirements have already been finalized. Thank you!", "plan": workflow_context.discovery_plan, "completed": True}

        if workflow_context.phase == "CONFIRMATION":
            return self._handle_confirmation_phase(workflow_context, client_message)
            
        # 0. Check for initialization message
        if client_message.strip() == "__INIT__":
            if workflow_context.is_continuation:
                if workflow_context.final_decision == "Accepted":
                    msg = f"Welcome back! Your project '{workflow_context.project_name}' has been Accepted by the Manager! Are you here to request updates or changes to the app?"
                else:
                    msg = f"Welcome back! I have loaded your existing requirements for '{workflow_context.project_name}'. Are we adding new features to the pipeline today?"
            else:
                msg = "Hello! I am your AI Project Analyst. To get started, please tell me a bit about the software project you'd like to build. What are your main goals? (Press and hold F8 to speak, or type below)"
                
            workflow_context.add_ai_message(msg)
            return {"response": msg, "plan": workflow_context.discovery_plan, "completed": False}

        # If it's a continuation, just extract facts, update the DB, and confirm
        if workflow_context.is_continuation:
            lower_msg = client_message.lower()
            if "no" in lower_msg or "that's all" in lower_msg or "nothing else" in lower_msg:
                workflow_context.phase = "COMPLETED"
                msg = "Perfect! Your project requirements are fully updated in the pipeline."
                workflow_context.add_ai_message(msg)
                return {"response": msg, "plan": workflow_context.discovery_plan, "completed": True}

            new_facts = self.knowledge_engine.extract_facts(workflow_context, client_message)
            if new_facts:
                workflow_context.requirement_facts.extend(new_facts)
                self._generate_final_requirements(workflow_context)
                msg = "I have successfully updated your project requirements with the new information! Is there anything else you'd like to add or change?"
            else:
                msg = "I didn't detect any specific new features in that message. Could you clarify what you'd like to add or change?"
            
            workflow_context.add_ai_message(msg)
            return {"response": msg, "plan": workflow_context.discovery_plan, "completed": False}

        # 1. Check if we need to plan the roadmap (first meaningful turn)
        if not workflow_context.discovery_plan:
            self.logger.info("Generating Initial Roadmap...")
            # We pass the entire conversation history instead of just the latest message
            history_text = workflow_context.get_conversation_text()
            if not history_text:
                history_text = client_message
                
            understanding, plan = self.planner.plan(history_text)
            
            if understanding.project_intent == "GREETING_OR_VAGUE":
                self.logger.info("Greeting or vague input detected.")
                # We do not set workflow_context.discovery_plan so it tries again next turn
                question = "Hello! I am your AI Project Analyst. Could you please tell me a bit more about the software project you'd like to build? (For example, an E-commerce app, a Healthcare system, etc.)"
                workflow_context.add_ai_message(question)
                return {"response": question, "plan": None}
                
            workflow_context.project_understanding = understanding
            workflow_context.discovery_plan = plan
            # Initialize questions asked counter
            if not hasattr(workflow_context, 'questions_asked'):
                workflow_context.questions_asked = 0
            
            # Extract any info from this first message
            self.knowledge_engine.update_knowledge(workflow_context, self.allowed_categories)
            
            next_topic = plan.topics[0]
            question = f"Great! I have planned {len(plan.topics)} modules to discuss for your {understanding.project_type}. Let's start with {next_topic.name}. {next_topic.goal} Could you tell me more about that?"
            
            workflow_context.add_ai_message(question)
            workflow_context.questions_asked += 1
            self.logger.info(f"[AI] {question}")
            return {"response": question, "plan": plan}

        # 2. Extract proactive knowledge from the client's answer across ALL modules
        self.knowledge_engine.update_knowledge(workflow_context, self.allowed_categories)

        # 3. Check hard limit (Max 10 questions)
        if hasattr(workflow_context, 'questions_asked') and workflow_context.questions_asked >= 10:
            return self._transition_to_confirmation(workflow_context, "We have covered a lot of ground today! ")

        # 4. Iterate through modules to find the first incomplete one
        current_topic_obj = None
        current_gap = None
        
        for topic in workflow_context.discovery_plan.topics:
            gap = self.gap_engine.analyze(workflow_context, topic.name)
            if not gap.completed:
                current_topic_obj = topic
                current_gap = gap
                break
                
        if not current_topic_obj:
            # All modules completed
            return self._transition_to_confirmation(workflow_context, "Excellent! I have all the information I need across all modules. ")

        # 5. Reason about the current gap and ask a question
        self.logger.info(f"Reasoning about topic: {current_topic_obj.name}")
        decision = self.reasoner.reason(workflow_context, current_gap)
        
        question = self.question_engine.generate(decision, workflow_context, current_topic_obj.name)
        
        if not question:
            question = f"Could you provide more details regarding {current_topic_obj.name}?"

        workflow_context.add_ai_message(question)
        workflow_context.questions_asked += 1
        
        self.logger.info(f"[AI] {question}")
        return {"response": question, "plan": workflow_context.discovery_plan, "completed": False}

    def _transition_to_confirmation(self, workflow_context, prefix_msg: str):
        workflow_context.phase = "CONFIRMATION"
        summary = self._generate_confirmation_summary(workflow_context)
        full_msg = prefix_msg + "Here is a summary of what I've gathered so far:\n\n" + summary + "\n\nDid I capture everything correctly, or is there anything else you'd like to add or change?"
        workflow_context.add_ai_message(full_msg)
        self.logger.info(f"[AI SUMMARY] Generating final summary for confirmation phase.")
        return {"response": full_msg, "plan": workflow_context.discovery_plan, "completed": False}

    def _handle_confirmation_phase(self, workflow_context, client_message):
        # Extract new facts just in case
        self.knowledge_engine.update_knowledge(workflow_context, self.allowed_categories)
        
        # Use LLM to classify if it's an approval or revision
        system_prompt = "You are a business analyst evaluating the client's confirmation response. Return valid JSON: {\"is_approved\": true/false}"
        user_prompt = f"Client message: {client_message}\nDoes the client approve the summary and say it's complete/ok without adding significant new requirements?"
        
        from src.services.llm_service import LLMService
        llm = LLMService()
        res = llm.generate_json(system_prompt, user_prompt)
        
        is_approved = False
        if res["success"] and res["content"]:
            is_approved = res["content"].get("is_approved", False)
            
        if is_approved:
            workflow_context.phase = "COMPLETED"
            self._generate_final_requirements(workflow_context)
            msg = "Fantastic! I have saved all the detailed requirements for the development team. Thank you for your time, the project qualification is now complete."
            workflow_context.add_ai_message(msg)
            return {"response": msg, "plan": workflow_context.discovery_plan, "completed": True}
        else:
            summary = self._generate_confirmation_summary(workflow_context)
            msg = "Got it, I've updated my notes! Here is the revised summary:\n\n" + summary + "\n\nDoes this look correct now?"
            workflow_context.add_ai_message(msg)
            return {"response": msg, "plan": workflow_context.discovery_plan, "completed": False}
            
    def _generate_confirmation_summary(self, workflow_context):
        lines = []
        topics = {}
        for fact in workflow_context.requirement_facts:
            topics.setdefault(fact.topic, []).append(fact)
            
        for topic, facts in topics.items():
            lines.append(f"**{topic}**")
            for f in facts:
                lines.append(f"- {f.category}: {f.key} ({f.value})")
            lines.append("")
        return "\n".join(lines) if lines else "No specific facts gathered yet."

    def _generate_final_requirements(self, workflow_context):
        from src.database.session import SessionLocal
        from src.entities.project_qualification import ProjectQualification
        
        data = {
            "project_understanding": vars(workflow_context.project_understanding) if workflow_context.project_understanding else {},
            "discovery_plan": [vars(t) for t in workflow_context.discovery_plan.topics] if workflow_context.discovery_plan else [],
            "requirement_facts": [vars(f) for f in workflow_context.requirement_facts],
            "conversation_history": [{"speaker": m.speaker, "message": m.message} for m in workflow_context.conversation_history]
        }
        
        db = SessionLocal()
        try:
            # Upsert
            qual = db.query(ProjectQualification).filter(
                ProjectQualification.client_id == workflow_context.client_id,
                ProjectQualification.project_name == workflow_context.project_name
            ).first()
            
            if qual:
                qual.requirements_json = data
                self.logger.info(f"Updated existing ProjectQualification for {workflow_context.project_name}")
            else:
                qual = ProjectQualification(
                    client_id=workflow_context.client_id,
                    project_name=workflow_context.project_name,
                    requirements_json=data
                )
                db.add(qual)
                self.logger.info(f"Created new ProjectQualification for {workflow_context.project_name}")
                
            db.commit()
        except Exception as e:
            db.rollback()
            self.logger.error(f"Error saving to database: {str(e)}")
        finally:
            db.close()
