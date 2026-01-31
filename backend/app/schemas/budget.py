from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, condecimal


class BudgetBase(BaseModel):
    category: str = Field(..., min_length=1, max_length=50)
    monthly_limit: condecimal(max_digits=12, decimal_places=2) = Field(..., gt=0)
    currency: str = Field(default="EUR", min_length=3, max_length=3)


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    monthly_limit: condecimal(max_digits=12, decimal_places=2) | None = Field(default=None, gt=0)
    currency: str | None = Field(default=None, min_length=3, max_length=3)


class BudgetRead(BudgetBase):
    id: int
    monthly_limit: Decimal

    model_config = ConfigDict(from_attributes=True)
