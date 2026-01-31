from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.models.transaction import Transaction


@dataclass
class AlertRow:
    category: str
    monthly_limit: object  # Decimal from DB
    spent: object  # Decimal from DB
    over_by: object  # Decimal from DB


def month_bounds(d: date) -> tuple[date, date]:
    # start = first day of month; end = last day of month
    start = date(d.year, d.month, 1)
    if d.month == 12:
        next_month = date(d.year + 1, 1, 1)
    else:
        next_month = date(d.year, d.month + 1, 1)
    end = next_month.fromordinal(next_month.toordinal() - 1)
    return start, end


def get_over_budget_alerts(db: Session, *, for_date: date) -> list[AlertRow]:
    start, end = month_bounds(for_date)

    # Spend per category this month
    spent_stmt = (
        select(
            Transaction.category.label("category"),
            func.coalesce(func.sum(Transaction.amount), 0).label("spent"),
        )
        .where(Transaction.tx_type == "expense")
        .where(Transaction.occurred_on >= start)
        .where(Transaction.occurred_on <= end)
        .group_by(Transaction.category)
        .subquery()
    )

    # Join budgets with spent
    stmt = (
        select(
            Budget.category,
            Budget.monthly_limit,
            func.coalesce(spent_stmt.c.spent, 0).label("spent"),
        )
        .select_from(Budget)
        .join(spent_stmt, spent_stmt.c.category == Budget.category, isouter=True)
    )

    rows = db.execute(stmt).all()

    alerts: list[AlertRow] = []
    for r in rows:
        spent = r.spent
        limit_ = r.monthly_limit
        if spent > limit_:
            alerts.append(
                AlertRow(
                    category=r.category, monthly_limit=limit_, spent=spent, over_by=spent - limit_
                )
            )

    # sort by most over budget
    alerts.sort(key=lambda x: x.over_by, reverse=True)
    return alerts
