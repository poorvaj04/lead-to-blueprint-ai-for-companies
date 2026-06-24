from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin


class Skill(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):
    """
    Stores company skills and technologies.
    """

    __tablename__ = "skill"

    skill_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    skill_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    skill_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    employee_skills = relationship(
    "EmployeeSkill",
    back_populates="skill",
    cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<Skill("
            f"skill_id={self.skill_id}, "
            f"name='{self.skill_name}')>"
        )