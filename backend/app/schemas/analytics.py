from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Bucket = Literal["necessary", "controllable", "unnecessary"]


class MoneyTotals(BaseModel):
    income: Decimal = Field(default=Decimal("0.00"))
    expense: Decimal = Field(default=Decimal("0.00"))
    net: Decimal = Field(default=Decimal("0.00"))

    model_config = ConfigDict(from_attributes=True)


class BucketTotal(BaseModel):
    bucket: Bucket | None
    expense: Decimal

    model_config = ConfigDict(from_attributes=True)


class CategoryTotal(BaseModel):
    category: str | None
    expense: Decimal

    model_config = ConfigDict(from_attributes=True)


class MonthlyTotal(BaseModel):
    month: str  # YYYY-MM
    income: Decimal
    expense: Decimal
    net: Decimal

    model_config = ConfigDict(from_attributes=True)


class AnalyticsSummary(BaseModel):
    totals: MoneyTotals
    by_bucket: list[BucketTotal]
    by_category: list[CategoryTotal]
    monthly: list[MonthlyTotal]

    model_config = ConfigDict(from_attributes=True)
