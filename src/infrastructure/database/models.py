from datetime import datetime

from uuid7 import UUID
from sqlalchemy import Index
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import String, DateTime, Integer, BigInteger, Boolean, Enum as SA_Enum, UUID as SA_UUID, JSON
from sqlalchemy.ext.declarative import declarative_base

from src.domain.events import EventType, EventStatus

Base = declarative_base()


class Gift(Base):
    __tablename__ = "gifts"
    __table_args__ = (
        Index("idx_gifts_date_stars", "date", "stars", "availability_total"),
        Index("idx_gifts_telegram_id", "telegram_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)

    availability_total: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(DateTime)
    stars: Mapped[int] = mapped_column(Integer)

    limited: Mapped[bool] = mapped_column(Boolean)
    is_upgradable: Mapped[bool] = mapped_column(Boolean)


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



