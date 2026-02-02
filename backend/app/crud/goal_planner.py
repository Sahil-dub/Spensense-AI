from __future__ import annotations

from datetime import date
from decimal import Decimal
from math import ceil

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def month_start(d: date) -> date:
    return date(d.year, d.month, 1)


def add_months(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    return date(y, m, 1)


def months_between_inclusive(start: date, end: date) -> int:
    # count months from start month to end month inclusive
    return (end.year - start.year) * 12 + (end.month - start.month) + 1


def get_recent_monthly_net(db: Session, *, months: int = 6) -> list[dict]:
    # returns list of {"month": "YYYY-MM", "income": Decimal, "expense": Decimal, "net": Decimal}
    month_expr = func.to_char(Transaction.occurred_on, "YYYY-MM").label("month")

    stmt = (
        select(
            month_expr,
            func.coalesce(
                func.sum(
                    case(
                        (Transaction.tx_type == "income", Transaction.amount),
                        else_=0,
                    )
                ),
                0,
            ).label("income"),
            func.coalesce(
                func.sum(
                    case(
                        (Transaction.tx_type == "expense", Transaction.amount),
                        else_=0,
                    )
                ),
                0,
            ).label("expense"),
        )
        .group_by(month_expr)
        .order_by(month_expr.desc())
        .limit(months)
    )

    rows = db.execute(stmt).all()
    out = []
    for r in rows:
        income = r.income or Decimal("0.00")
        expense = r.expense or Decimal("0.00")
        out.append(
            {
                "month": r.month,
                "income": income,
                "expense": expense,
                "net": income - expense,
            }
        )
    return list(reversed(out))


def get_top_spend_categories(
    db: Session,
    *,
    date_from: date,
    date_to: date,
    buckets: list[str],
    top_n: int = 5,
) -> list[dict]:
    stmt = (
        select(
            Transaction.category.label("category"),
            func.coalesce(func.sum(Transaction.amount), 0).label("expense"),
        )
        .where(Transaction.tx_type == "expense")
        .where(Transaction.occurred_on >= date_from)
        .where(Transaction.occurred_on <= date_to)
        .where(Transaction.bucket.in_(buckets))
        .group_by(Transaction.category)
        .order_by(func.coalesce(func.sum(Transaction.amount), 0).desc())
        .limit(top_n)
    )

    rows = db.execute(stmt).all()
    return [{"category": r.category, "expense": r.expense or Decimal("0.00")} for r in rows]


def plan_goal(
    db: Session,
    *,
    target_amount: Decimal,
    target_date: date,
    history_months: int = 6,
) -> dict:
    today = date.today()
    start_month = month_start(today)
    end_month = month_start(target_date)

    months_remaining = months_between_inclusive(start_month, end_month)
    required_monthly = (target_amount / Decimal(months_remaining)).quantize(Decimal("0.01"))

    monthly = get_recent_monthly_net(db, months=history_months)
    if monthly:
        avg_net = (
            sum((m["net"] for m in monthly), Decimal("0.00")) / Decimal(len(monthly))
        ).quantize(Decimal("0.01"))
    else:
        avg_net = Decimal("0.00")

    feasible = avg_net >= required_monthly and avg_net > 0

    shortfall = (
        (required_monthly - avg_net).quantize(Decimal("0.01")) if not feasible else Decimal("0.00")
    )

    # If not feasible but avg_net > 0, estimate projected months to reach target
    projected_months = None
    projected_date = None
    if avg_net > 0:
        projected_months = int(ceil((target_amount / avg_net)))
        projected_date = add_months(start_month, projected_months - 1)  # inclusive months

    # Suggest where to cut based on last 30 days spend in controllable/unnecessary buckets
    # (simple heuristic; later we can use month boundaries)
    date_from = today.replace(day=1)
    # end of current month approx: take next month start - 1 day
    next_month = add_months(date_from, 1)
    date_to = date(next_month.year, next_month.month, 1).fromordinal(next_month.toordinal() - 1)

    top_cuts = get_top_spend_categories(
        db,
        date_from=date_from,
        date_to=date_to,
        buckets=["controllable", "unnecessary"],
        top_n=5,
    )

    return {
        "months_remaining": months_remaining,
        "required_monthly_saving": required_monthly,
        "avg_monthly_net_saving": avg_net,
        "feasible": feasible,
        "monthly_shortfall": shortfall,
        "projected_months_if_unchanged": projected_months,
        "projected_goal_month_if_unchanged": (
            projected_date.strftime("%Y-%m") if projected_date else None
        ),
        "suggested_cut_targets": top_cuts,
        "history_months_used": history_months,
    }
