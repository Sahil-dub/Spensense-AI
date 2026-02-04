from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def get_daily_series(db: Session, *, date_from: date, date_to: date) -> list[dict]:
    # Group by occurred_on (daily)
    stmt = (
        select(
            Transaction.occurred_on.label("d"),
            func.coalesce(
                func.sum(case((Transaction.tx_type == "income", Transaction.amount), else_=0)),
                0,
            ).label("income"),
            func.coalesce(
                func.sum(case((Transaction.tx_type == "expense", Transaction.amount), else_=0)),
                0,
            ).label("expense"),
        )
        .where(Transaction.occurred_on >= date_from)
        .where(Transaction.occurred_on <= date_to)
        .group_by(Transaction.occurred_on)
        .order_by(Transaction.occurred_on.asc())
    )

    rows = db.execute(stmt).all()

    out: list[dict] = []
    for r in rows:
        income = r.income or Decimal("0.00")
        expense = r.expense or Decimal("0.00")
        out.append(
            {
                "date": r.d.isoformat(),
                "income": income,
                "expense": expense,
                "net": income - expense,
            }
        )
    return out
