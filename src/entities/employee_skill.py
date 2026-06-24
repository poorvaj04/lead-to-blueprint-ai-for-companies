from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin


class EmployeeSkill(
    BaseEntity,
    TimestampMixin
):
    """
    Maps employees to their skills.
    """

    __tablename__ = "employee_skill"

    employee_skill_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.employee_id"),
        nullable=False
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skill.skill_id"),
        nullable=False
    )

    proficiency_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    employee = relationship(
        "Employee",
        back_populates="employee_skills"
    )

    skill = relationship(
        "Skill",
        back_populates="employee_skills"
    )

    def __repr__(self):
        return (
            f"<EmployeeSkill("
            f"employee_id={self.employee_id}, "
            f"skill_id={self.skill_id}, "
            f"level={self.proficiency_level})>"
        )