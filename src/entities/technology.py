from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin


class Technology(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):
    """
    Stores technologies supported by the company.
    """

    __tablename__ = "technology"

    technology_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    technology_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    technology_category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    version: Mapped[str] = mapped_column(
        String(30),
        nullable=True
    )

    def __repr__(self):

        return (
            f"<Technology("
            f"technology_id={self.technology_id}, "
            f"name='{self.technology_name}')>"
        )