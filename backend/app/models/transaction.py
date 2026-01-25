from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    tx_type: Mapped[str] = mapped_column(String(10), nullable=False)  # income | expense
    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")

    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bucket: Mapped[str | None] = mapped_column(String(20), nullable=True)

    occurred_on: Mapped[date] = mapped_column(Date, nullable=False)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        CheckConstraint("tx_type IN ('income','expense')", name="ck_transactions_tx_type"),
    )
