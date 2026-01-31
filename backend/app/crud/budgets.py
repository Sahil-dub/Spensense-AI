from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


def create_budget(db: Session, payload: BudgetCreate) -> Budget:
    b = Budget(
        category=payload.category,
        monthly_limit=payload.monthly_limit,
        currency=payload.currency.upper(),
    )
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


def get_budget(db: Session, budget_id: int) -> Budget | None:
    return db.get(Budget, budget_id)


def get_budget_by_category(db: Session, category: str) -> Budget | None:
    stmt = select(Budget).where(Budget.category == category)
    return db.execute(stmt).scalars().first()


def list_budgets(db: Session, *, limit: int = 50, offset: int = 0) -> list[Budget]:
    stmt = select(Budget).order_by(Budget.category.asc()).offset(offset).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_budget(db: Session, b: Budget, payload: BudgetUpdate) -> Budget:
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        if k == "currency" and v is not None:
            v = v.upper()
        setattr(b, k, v)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


def delete_budget(db: Session, b: Budget) -> None:
    db.delete(b)
    db.commit()
