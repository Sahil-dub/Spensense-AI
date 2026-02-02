from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CutTarget(BaseModel):
    category: str | None
    expense: Decimal

    model_config = ConfigDict(from_attributes=True)


class GoalPlanResponse(BaseModel):
    months_remaining: int
    required_monthly_saving: Decimal
    avg_monthly_net_saving: Decimal
    feasible: bool
    monthly_shortfall: Decimal
    projected_months_if_unchanged: int | None
    projected_goal_month_if_unchanged: str | None  # YYYY-MM
    suggested_cut_targets: list[CutTarget]
    history_months_used: int

    model_config = ConfigDict(from_attributes=True)
