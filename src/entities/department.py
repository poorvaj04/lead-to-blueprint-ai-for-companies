from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin
from sqlalchemy.orm import relationship


class Department(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):
    """
    Stores company departments.
    """

    __tablename__ = "department"

    department_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    department_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    department_description: Mapped[str] = mapped_column(
        String(300),
        nullable=True
    )
    employees = relationship(
    "Employee",
    back_populates="department",
    cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<Department("
            f"department_id={self.department_id}, "
            f"name='{self.department_name}')>"
        )