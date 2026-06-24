from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin
from src.schemas.availability_status import AvailabilityStatus


class EmployeeAvailability(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):

    __tablename__ = "employee_availability"

    availability_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employee.employee_id"),
        unique=True,
        nullable=False
    )

    availability_status: Mapped[AvailabilityStatus] = mapped_column(
        Enum(AvailabilityStatus),
        default=AvailabilityStatus.AVAILABLE,
        nullable=False
    )

    available_hours_per_week: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    current_project: Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )

    employee = relationship(
        "Employee",
        back_populates="availability"
    )

    def __repr__(self):

        return (
            f"<EmployeeAvailability("
            f"employee_id={self.employee_id}, "
            f"status='{self.availability_status.value}')>"
        )