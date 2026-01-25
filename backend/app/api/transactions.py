from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.crud.transactions import (
    create_transaction,
    delete_transaction,
    get_transaction,
    list_transactions,
    update_transaction,
)
from app.db.session import get_db
from app.schemas.transaction import TransactionCreate, TransactionRead, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def create_tx(payload: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, payload)


@router.get("", response_model=list[TransactionRead])
def list_txs(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    tx_type: str | None = Query(None, pattern="^(income|expense)$"),
    category: str | None = None,
    bucket: str | None = Query(None, pattern="^(necessary|controllable|unnecessary)$"),
    date_from: date | None = None,
    date_to: date | None = None,
):
    return list_transactions(
        db,
        limit=limit,
        offset=offset,
        tx_type=tx_type,
        category=category,
        bucket=bucket,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{tx_id}", response_model=TransactionRead)
def get_tx(tx_id: int, db: Session = Depends(get_db)):
    tx = get_transaction(db, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


@router.put("/{tx_id}", response_model=TransactionRead)
def update_tx(tx_id: int, payload: TransactionUpdate, db: Session = Depends(get_db)):
    tx = get_transaction(db, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return update_transaction(db, tx, payload)


@router.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tx(tx_id: int, db: Session = Depends(get_db)):
    tx = get_transaction(db, tx_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    delete_transaction(db, tx)
    return None
