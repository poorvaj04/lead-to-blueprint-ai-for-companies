from src.utils.logger import get_logger
from src.database.session import SessionLocal
from src.entities.manager_notification import ManagerNotification
from src.dtos.crm_report import CRMReport

class NotificationAgent:
    def __init__(self):
        self.logger = get_logger("NotificationAgent")

    def process(self, crm_report: CRMReport):
        self.logger.info("Goal: Notify the engineering manager of the final project analysis.")
        self.logger.info("Reason: The project has been fully qualified and a decision was reached.")
        
        db = SessionLocal()
        try:
            existing_notif = db.query(ManagerNotification).filter_by(qualification_id=crm_report.qualification_id).first()
            if existing_notif:
                existing_notif.status = "UNREAD"
                existing_notif.crm_report = crm_report.model_dump()
            else:
                notif = ManagerNotification(
                    qualification_id=crm_report.qualification_id,
                    status="UNREAD",
                    crm_report=crm_report.model_dump()
                )
                db.add(notif)
            
            db.commit()
            
            self.logger.info("Decision: Notification row safely upserted in the database.")
            self.logger.info("Action: Firing mock Slack/Email alert to managers.")
            self.logger.info("="*40)
            self.logger.info(f"EMAIL MOCK: To Manager - Project '{crm_report.project_name}' has been {crm_report.final_decision}.")
            self.logger.info("="*40)
        except Exception as e:
            self.logger.error(f"Failed to create manager notification: {e}")
            db.rollback()
        finally:
            db.close()
