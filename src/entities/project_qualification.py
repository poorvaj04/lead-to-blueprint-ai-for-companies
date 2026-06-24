from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin

class ProjectQualification(BaseEntity, TimestampMixin):
    """
    The single source of truth for the multi-agent qualification pipeline.
    Links exactly 1 Client to Multiple distinct Projects.
    """

    __tablename__ = "project_qualification"

    qualification_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.client_id"),
        nullable=False
    )

    project_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    # Pipeline Storage Columns
    requirements_json: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )
    
    complexity_score: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    
    complexity_report: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )
    
    feasibility_report: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )
    
    risk_analysis: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )
    
    final_decision: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    # Enforce exact separation: A client cannot have duplicate projects with the same name.
    __table_args__ = (
        UniqueConstraint('client_id', 'project_name', name='uq_client_project'),
    )

    # Relationships
    client = relationship("Client")

    def __repr__(self):
        return (
            f"<ProjectQualification("
            f"id={self.qualification_id}, "
            f"client_id={self.client_id}, "
            f"project='{self.project_name}')>"
        )
