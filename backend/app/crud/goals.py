from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.schemas.goal import GoalCreate


def create_goal(db: Session, payload: GoalCreate) -> Goal:
    g = Goal(
        name=payload.name,
        target_amount=payload.target_amount,
        currency=payload.currency.upper(),
        target_date=payload.target_date,
    )
    db.add(g)
    db.commit()
    db.refresh(g)
    return g


def get_goal(db: Session, goal_id: int) -> Goal | None:
    return db.get(Goal, goal_id)


def list_goals(db: Session, *, limit: int = 50, offset: int = 0) -> list[Goal]:
    stmt = select(Goal).order_by(Goal.target_date.asc(), Goal.id.asc()).offset(offset).limit(limit)
    return list(db.execute(stmt).scalars().all())


def delete_goal(db: Session, g: Goal) -> None:
    db.delete(g)
    db.commit()
