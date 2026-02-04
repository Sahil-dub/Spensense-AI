from __future__ import annotations

from datetime import date, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.analytics.daily import get_daily_series
from app.crud.analytics.summary import get_by_bucket, get_by_category, get_monthly, get_totals
from app.db.session import get_db
from app.schemas.analytics import AnalyticsSummary
from app.schemas.daily_analytics import DailySeries

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/daily", response_model=DailySeries)
def analytics_daily(
    db: Session = Depends(get_db),
    date_from: date | None = None,
    date_to: date | None = None,
):
    # Default: last 30 days
    if date_to is None:
        date_to = date.today()
    if date_from is None:
        date_from = date_to - timedelta(days=30)

    if date_from > date_to:
        raise HTTPException(status_code=400, detail="date_from must be <= date_to")

    points = get_daily_series(db, date_from=date_from, date_to=date_to)
    return {"points": points}


@router.get("/summary", response_model=AnalyticsSummary)
def analytics_summary(
    db: Session = Depends(get_db),
    date_from: date | None = None,
    date_to: date | None = None,
    top_categories: int = Query(10, ge=1, le=50),
    months: int = Query(12, ge=1, le=60),
):
    totals = get_totals(db, date_from=date_from, date_to=date_to)
    by_bucket = get_by_bucket(db, date_from=date_from, date_to=date_to)
    by_category = get_by_category(db, top_n=top_categories, date_from=date_from, date_to=date_to)
    monthly = get_monthly(db, months=months, date_from=date_from, date_to=date_to)

    return {
        "totals": totals,
        "by_bucket": by_bucket,
        "by_category": by_category,
        "monthly": monthly,
    }
