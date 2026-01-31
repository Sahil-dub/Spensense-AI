from __future__ import annotations
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict

Bucket = Literal["necessary", "controllable", "unnecessary"]

class MoneyTotals(BaseModel):
    income: Decimal = Field(default=Decimal("0.00"))
    expenses: Decimal = Field(default=Decimal("0.00"))
    net: Decimal = Field(default=Decimal("0.00"))

    model_config = ConfigDict(from_attributes=True)

class BucketTotals(BaseModel):
    bucket: Bucket | None
    expenses: Decimal

    model_config = ConfigDict(from_attributes=True)

class CategoryTotals(BaseModel):
    category_id: str | None
    expenses: Decimal

    model_config = ConfigDict(from_attributes=True)

class MonthlyTotals(BaseModel):
    month: str  #YYYY-MM
    income: Decimal
    expenses: Decimal
    net: Decimal

    model_config = ConfigDict(from_attributes=True)

class AnalyticsSummary(BaseModel):
    total: MoneyTotals
    by_bucket: list[BucketTotals]
    by_category: list[CategoryTotals]
    monthly: list[MonthlyTotals]

    model_config = ConfigDict(from_attributes=True)

    