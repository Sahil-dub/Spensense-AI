from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DailyPoint(BaseModel):
    date: str  # YYYY-MM-DD
    income: Decimal
    expense: Decimal
    net: Decimal

    model_config = ConfigDict(from_attributes=True)


class DailySeries(BaseModel):
    points: list[DailyPoint]

    model_config = ConfigDict(from_attributes=True)
