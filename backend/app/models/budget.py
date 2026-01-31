from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # single-user MVP: one budget per category
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    monthly_limit: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)

    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")

    __table_args__ = (UniqueConstraint("category", name="uq_budgets_category"),)
