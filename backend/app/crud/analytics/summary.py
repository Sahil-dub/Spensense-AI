from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import DATE, TEXT
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def _d0(x) -> Decimal:
    return x if x is not None else Decimal("0.00")


def get_totals(db: Session, *, date_from: date | None = None, date_to: date | None = None) -> dict:
    stmt = select(
        func.coalesce(func.sum(func.case((Transaction.tx_type == "income", Transaction.amount), else_=0)), 0).label(
            "income"
        ),
        func.coalesce(func.sum(func.case((Transaction.tx_type == "expense", Transaction.amount), else_=0)), 0).label(
            "expense"
        ),
    )

    if date_from:
        stmt = stmt.where(Transaction.occurred_on >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.occurred_on <= date_to)

    income, expense = db.execute(stmt).one()
    income = _d0(income)
    expense = _d0(expense)
    return {"income": income, "expense": expense, "net": income - expense}


def get_by_bucket(
    db: Session, *, date_from: date | None = None, date_to: date | None = None
) -> list[dict]:
    stmt = (
        select(
            Transaction.bucket.label("bucket"),
            func.coalesce(func.sum(Transaction.amount), 0).label("expense"),
        )
        .where(Transaction.tx_type == "expense")
        .group_by(Transaction.bucket)
        .order_by(func.coalesce(func.sum(Transaction.amount), 0).desc())
    )

    if date_from:
        stmt = stmt.where(Transaction.occurred_on >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.occurred_on <= date_to)

    rows = db.execute(stmt).all()
    return [{"bucket": r.bucket, "expense": _d0(r.expense)} for r in rows]


def get_by_category(
    db: Session,
    *,
    top_n: int = 10,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[dict]:
    stmt = (
        select(
            Transaction.category.label("category"),
            func.coalesce(func.sum(Transaction.amount), 0).label("expense"),
        )
        .where(Transaction.tx_type == "expense")
        .group_by(Transaction.category)
        .order_by(func.coalesce(func.sum(Transaction.amount), 0).desc())
        .limit(top_n)
    )

    if date_from:
        stmt = stmt.where(Transaction.occurred_on >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.occurred_on <= date_to)

    rows = db.execute(stmt).all()
    return [{"category": r.category, "expense": _d0(r.expense)} for r in rows]


def get_monthly(
    db: Session, *, months: int = 12, date_from: date | None = None, date_to: date | None = None
) -> list[dict]:
    # Postgres: to_char(date, 'YYYY-MM') for grouping
    month_expr = func.to_char(Transaction.occurred_on, "YYYY-MM").label("month")

    stmt = (
        select(
            month_expr,
            func.coalesce(func.sum(func.case((Transaction.tx_type == "income", Transaction.amount), else_=0)), 0).label(
                "income"
            ),
            func.coalesce(func.sum(func.case((Transaction.tx_type == "expense", Transaction.amount), else_=0)), 0).label(
                "expense"
            ),
        )
        .group_by(month_expr)
        .order_by(month_expr.desc())
        .limit(months)
    )

    if date_from:
        stmt = stmt.where(Transaction.occurred_on >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.occurred_on <= date_to)

    rows = db.execute(stmt).all()

    # Convert to dicts and compute net; reverse to chronological ascending
    out = []
    for r in rows:
        income = _d0(r.income)
        expense = _d0(r.expense)
        out.append({"month": r.month, "income": income, "expense": expense, "net": income - expense})

    return list(reversed(out))
