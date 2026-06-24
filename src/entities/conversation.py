from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from src.database.base import BaseEntity
from src.database.mixins import TimestampMixin, StatusMixin
from src.schemas.conversation_status import ConversationStatus


class Conversation(
    BaseEntity,
    TimestampMixin,
    StatusMixin
):

    __tablename__ = "conversation"

    conversation_id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    inquiry_id: Mapped[int] = mapped_column(
        ForeignKey("inquiry.inquiry_id"),
        nullable=False
    )

    audio_file_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    raw_transcript: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    confirmed_transcript: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    conversation_summary: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    call_duration_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    call_status: Mapped[ConversationStatus] = mapped_column(
        Enum(ConversationStatus),
        default=ConversationStatus.STARTED,
        nullable=False
    )

    inquiry = relationship(
        "Inquiry",
        back_populates="conversation"
    )

    def __repr__(self):

        return (
            f"<Conversation("
            f"conversation_id={self.conversation_id}, "
            f"status='{self.call_status.value}')>"
        )