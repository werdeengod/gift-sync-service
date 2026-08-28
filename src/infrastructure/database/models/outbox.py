from uuid7 import UUID
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import DateTime, Enum as SA_Enum, UUID as SA_UUID, JSON
from src.infrastructure.database import Base

from src.domain.events import EventType, EventStatus


class Outbox(Base):
    __tablename__ = "outbox"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[UUID] = mapped_column(SA_UUID(as_uuid=True), unique=True, index=True)
    event_type: Mapped[EventType] = mapped_column(SA_Enum(EventType, name="event_type"))
    occurred_at: Mapped[DateTime] = mapped_column(DateTime)
    payload: Mapped[dict] = mapped_column(JSON)

    sent_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    status: Mapped[EventStatus] = mapped_column(
        SA_Enum(EventStatus, name="event_status"),
        server_default=EventStatus.PENDING.value,
        index=True
    )
