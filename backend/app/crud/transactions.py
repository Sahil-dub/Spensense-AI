from __future__ import annotations

from datetime import date

from sqlalchemy import Select, delete, select
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate


def create_transaction(db: Session, payload: TransactionCreate) -> Transaction:
    tx = Transaction(**payload.model_dump())
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def get_transaction(db: Session, tx_id: int) -> Transaction | None:
    return db.get(Transaction, tx_id)


def list_transactions(
    db: Session,
    *,
    limit: int = 50,
    offset: int = 0,
    tx_type: str | None = None,
    category: str | None = None,
    bucket: str | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
) -> list[Transaction]:
    stmt: Select[tuple[Transaction]] = select(Transaction).order_by(Transaction.occurred_on.desc(), Transaction.id.desc())

    if tx_type:
        stmt = stmt.where(Transaction.tx_type == tx_type)
    if category:
        stmt = stmt.where(Transaction.category == category)
    if bucket:
        stmt = stmt.where(Transaction.bucket == bucket)
    if date_from:
        stmt = stmt.where(Transaction.occurred_on >= date_from)
    if date_to:
        stmt = stmt.where(Transaction.occurred_on <= date_to)

    stmt = stmt.offset(offset).limit(limit)
    return list(db.execute(stmt).scalars().all())


def update_transaction(db: Session, tx: Transaction, payload: TransactionUpdate) -> Transaction:
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(tx, k, v)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx


def delete_transaction(db: Session, tx: Transaction) -> None:
    db.delete(tx)
    db.commit()
