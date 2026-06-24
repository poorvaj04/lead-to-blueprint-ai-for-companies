from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin


class Requirement(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):

    __tablename__ = "requirement"

    requirement_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    inquiry_id: Mapped[int] = mapped_column(
        ForeignKey("inquiry.inquiry_id"),
        unique=True,
        nullable=False
    )

    project_title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    project_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    business_problem: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    functional_requirements: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    non_functional_requirements: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    constraints: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    estimated_timeline: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    estimated_budget: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )

    completeness_score: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    inquiry = relationship(
        "Inquiry",
        back_populates="requirement"
    )

    def __repr__(self):

        return (
            f"<Requirement("
            f"requirement_id={self.requirement_id}, "
            f"project='{self.project_title}', "
            f"score={self.completeness_score})>"
        )