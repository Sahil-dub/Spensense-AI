from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, condecimal

TxType = Literal["income", "expense"]
Bucket = Literal["necessary", "controllable", "unnecessary"]


class TransactionBase(BaseModel):
    tx_type: TxType
    amount: condecimal(max_digits=12, decimal_places=2) = Field(..., gt=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)

    category: str | None = Field(default=None, max_length=50)
    bucket: Bucket | None = None

    occurred_on: date
    note: str | None = Field(default=None, max_length=255)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    tx_type: TxType | None = None
    amount: condecimal(max_digits=12, decimal_places=2) | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)

    category: str | None = Field(default=None, max_length=50)
    bucket: Bucket | None = None

    occurred_on: date | None = None
    note: str | None = Field(default=None, max_length=255)


class TransactionRead(TransactionBase):
    id: int

    # ensure Decimal is serialized nicely
    amount: Decimal

    class Config:
        from_attributes = True
