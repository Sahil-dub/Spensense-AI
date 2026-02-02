from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud.goal_planner import plan_goal
from app.crud.goals import get_goal
from app.db.session import get_db
from app.schemas.goal_plan import GoalPlanResponse

router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("/{goal_id}/plan", response_model=GoalPlanResponse)
def goal_plan(
    goal_id: int,
    db: Session = Depends(get_db),
    history_months: int = Query(6, ge=1, le=24),
):
    g = get_goal(db, goal_id)
    if not g:
        raise HTTPException(status_code=404, detail="Goal not found")

    data = plan_goal(
        db,
        target_amount=g.target_amount,
        target_date=g.target_date,
        history_months=history_months,
    )
    return data
