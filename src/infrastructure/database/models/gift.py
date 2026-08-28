from datetime import datetime

from sqlalchemy import Index
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import String, DateTime, Integer, BigInteger, Boolean
from src.infrastructure.database import Base


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
