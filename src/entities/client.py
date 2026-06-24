from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin


class Client(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):
    """
    Stores client/company information.
    """

    __tablename__ = "client"

    # Primary Key
    client_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    # Auth Details
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Company Details
    company_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    contact_person: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Contact Details
    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    country_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    inquiries = relationship(
    "Inquiry",
    back_populates="client",
    cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Client("
            f"client_id={self.client_id}, "
            f"company_name='{self.company_name}', "
            f"contact_person='{self.contact_person}')>"
        )