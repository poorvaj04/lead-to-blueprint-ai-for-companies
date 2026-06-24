from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin
from src.schemas.inquiry_status import InquiryStatus


class Inquiry(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):
    """
    Represents a project inquiry submitted by a client.
    """

    __tablename__ = "inquiry"

    inquiry_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("client.client_id"),
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

    status: Mapped[InquiryStatus] = mapped_column(
        Enum(InquiryStatus),
        default=InquiryStatus.NEW,
        nullable=False
    )

    client = relationship(
        "Client",
        back_populates="inquiries"
    )
    conversation = relationship(
    "Conversation",
    back_populates="inquiry",
    uselist=False,
    cascade="all, delete-orphan"
    )
    requirement = relationship(
    "Requirement",
    back_populates="inquiry",
    uselist=False,
    cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Inquiry("
            f"inquiry_id={self.inquiry_id}, "
            f"title='{self.project_title}', "
            f"status='{self.status.value}')>"
        )