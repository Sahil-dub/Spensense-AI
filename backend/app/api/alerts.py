from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud.alerts import get_over_budget_alerts
from app.db.session import get_db
from app.schemas.alerts import AlertsResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=AlertsResponse)
def alerts(
    db: Session = Depends(get_db),
    month: str | None = Query(None, description="YYYY-MM. Defaults to current month."),
):
    if month:
        # Parse YYYY-MM
        for_date = datetime.strptime(month + "-01", "%Y-%m-%d").date()
    else:
        for_date = date.today()

    rows = get_over_budget_alerts(db, for_date=for_date)
    return {
        "month": for_date.strftime("%Y-%m"),
        "alerts": [
            {
                "category": r.category,
                "monthly_limit": r.monthly_limit,
                "spent": r.spent,
                "over_by": r.over_by,
            }
            for r in rows
        ],
    }
