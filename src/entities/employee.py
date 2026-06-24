from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin


class Employee(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):

    __tablename__ = "employee"

    employee_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("department.department_id"),
        nullable=False
    )

    employee_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    years_of_experience: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    employment_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    department = relationship(
        "Department",
        back_populates="employees"
    )
    employee_skills = relationship(
    "EmployeeSkill",
    back_populates="employee",
    cascade="all, delete-orphan"
    )
    availability = relationship(
    "EmployeeAvailability",
    back_populates="employee",
    uselist=False,
    cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<Employee("
            f"employee_id={self.employee_id}, "
            f"name='{self.employee_name}')>"
        )