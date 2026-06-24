from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin
from src.schemas.infrastructure_status import InfrastructureStatus


class Infrastructure(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):
    """
    Stores company infrastructure resources.
    """

    __tablename__ = "infrastructure"

    infrastructure_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    resource_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    infrastructure_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="IT & Corporate Infrastructure"
    )

    resource_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    availability_status: Mapped[InfrastructureStatus] = mapped_column(
        Enum(InfrastructureStatus),
        default=InfrastructureStatus.AVAILABLE,
        nullable=False
    )

    def __repr__(self):

        return (
            f"<Infrastructure("
            f"infrastructure_id={self.infrastructure_id}, "
            f"resource='{self.resource_name}')>"
        )