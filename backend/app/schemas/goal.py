from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, condecimal


class GoalBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    target_amount: condecimal(max_digits=12, decimal_places=2) = Field(..., gt=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)
    target_date: date


class GoalCreate(GoalBase):
    pass


class GoalRead(GoalBase):
    id: int
    target_amount: Decimal
    created_on: date

    model_config = ConfigDict(from_attributes=True)
