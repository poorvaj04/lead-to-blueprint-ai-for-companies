from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin
from src.schemas.project_status import ProjectStatus


class CompletedProject(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):
    """
    Stores previously completed company projects.
    """

    __tablename__ = "completed_project"

    completed_project_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    project_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    project_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    client_domain: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    duration_months: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    team_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    project_status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus),
        nullable=False
    )

    def __repr__(self):

        return (
            f"<CompletedProject("
            f"id={self.completed_project_id}, "
            f"name='{self.project_name}')>"
        )