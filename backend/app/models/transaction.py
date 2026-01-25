from sqlalchemy import String, Date, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    tx_type: Mapped[str] = mapped_column(String(10), nullable=False)  # income | expense
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="EUR")

    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    bucket: Mapped[str | None] = mapped_column(String(20), nullable=True)  # necessary/controllable/unnecessary

    occurred_on: Mapped[str] = mapped_column(Date, nullable=False)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)

    __table_args__ = (
        CheckConstraint("tx_type IN ('income','expense')", name="ck_transactions_tx_type"),
    )
