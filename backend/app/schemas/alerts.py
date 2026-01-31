from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class BudgetAlert(BaseModel):
    category: str
    monthly_limit: Decimal
    spent: Decimal
    over_by: Decimal

    model_config = ConfigDict(from_attributes=True)


class AlertsResponse(BaseModel):
    month: str  # YYYY-MM
    alerts: list[BudgetAlert]

    model_config = ConfigDict(from_attributes=True)
