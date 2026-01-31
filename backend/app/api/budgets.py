from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.budgets import (
    create_budget,
    delete_budget,
    get_budget,
    list_budgets,
    update_budget,
)
from app.db.session import get_db
from app.schemas.budget import BudgetCreate, BudgetRead, BudgetUpdate

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def create_budget_endpoint(payload: BudgetCreate, db: Session = Depends(get_db)):
    # Enforce EUR-only for MVP
    if payload.currency.upper() != "EUR":
        raise HTTPException(status_code=400, detail="Only EUR is supported in MVP")

    try:
        return create_budget(db, payload)
    except IntegrityError:
        db.rollback()
    raise HTTPException(
        status_code=409,
        detail="Budget already exists for this category",
    ) from None


@router.get("", response_model=list[BudgetRead])
def list_budgets_endpoint(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return list_budgets(db, limit=limit, offset=offset)


@router.get("/{budget_id}", response_model=BudgetRead)
def get_budget_endpoint(budget_id: int, db: Session = Depends(get_db)):
    b = get_budget(db, budget_id)
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    return b


@router.put("/{budget_id}", response_model=BudgetRead)
def update_budget_endpoint(budget_id: int, payload: BudgetUpdate, db: Session = Depends(get_db)):
    if payload.currency and payload.currency.upper() != "EUR":
        raise HTTPException(status_code=400, detail="Only EUR is supported in MVP")

    b = get_budget(db, budget_id)
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    return update_budget(db, b, payload)


@router.delete("/{budget_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_budget_endpoint(budget_id: int, db: Session = Depends(get_db)):
    b = get_budget(db, budget_id)
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    delete_budget(db, b)
    return None
