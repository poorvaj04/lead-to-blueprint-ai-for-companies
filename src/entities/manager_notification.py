from sqlalchemy import ForeignKey, String, JSON, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin

class ManagerNotification(BaseEntity, TimestampMixin):
    __tablename__ = "manager_notification"

    notification_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    qualification_id: Mapped[int] = mapped_column(
        ForeignKey("project_qualification.qualification_id"),
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="UNREAD")
    crm_report: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    qualification = relationship("ProjectQualification")
    
    def __repr__(self):
        return f"<ManagerNotification(id={self.notification_id}, qualification_id={self.qualification_id}, status='{self.status}')>"
