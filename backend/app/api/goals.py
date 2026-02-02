from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.goals import create_goal, delete_goal, get_goal, list_goals
from app.db.session import get_db
from app.schemas.goal import GoalCreate, GoalRead

router = APIRouter(prefix="/goals", tags=["goals"])


@router.post("", response_model=GoalRead, status_code=status.HTTP_201_CREATED)
def create_goal_endpoint(payload: GoalCreate, db: Session = Depends(get_db)):
    if payload.currency.upper() != "EUR":
        raise HTTPException(status_code=400, detail="Only EUR is supported in MVP")
    if payload.target_date <= date.today():
        raise HTTPException(status_code=400, detail="target_date must be in the future")
    return create_goal(db, payload)


@router.get("", response_model=list[GoalRead])
def list_goals_endpoint(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return list_goals(db, limit=limit, offset=offset)


@router.get("/{goal_id}", response_model=GoalRead)
def get_goal_endpoint(goal_id: int, db: Session = Depends(get_db)):
    g = get_goal(db, goal_id)
    if not g:
        raise HTTPException(status_code=404, detail="Goal not found")
    return g


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal_endpoint(goal_id: int, db: Session = Depends(get_db)):
    g = get_goal(db, goal_id)
    if not g:
        raise HTTPException(status_code=404, detail="Goal not found")
    delete_goal(db, g)
    return None
