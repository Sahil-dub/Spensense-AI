from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_goal_plan_returns_shape():
    # Seed some net savings: income 1000, expenses 600 -> avg_net positive
    today = date.today()
    occurred_on = str(today)

    client.post(
        "/transactions",
        json={
            "tx_type": "income",
            "amount": 1000,
            "currency": "EUR",
            "category": "salary",
            "bucket": None,
            "occurred_on": occurred_on,
        },
    )
    client.post(
        "/transactions",
        json={
            "tx_type": "expense",
            "amount": 400,
            "currency": "EUR",
            "category": "rent",
            "bucket": "necessary",
            "occurred_on": occurred_on,
        },
    )
    client.post(
        "/transactions",
        json={
            "tx_type": "expense",
            "amount": 200,
            "currency": "EUR",
            "category": "dining_out",
            "bucket": "controllable",
            "occurred_on": occurred_on,
        },
    )

    # Create a goal 3 months ahead
    future = today + timedelta(days=90)
    res_goal = client.post(
        "/goals",
        json={"name": "Trip", "target_amount": 300, "currency": "EUR", "target_date": str(future)},
    )
    assert res_goal.status_code == 201, res_goal.text
    goal_id = res_goal.json()["id"]

    res = client.get(f"/goals/{goal_id}/plan?history_months=6")
    assert res.status_code == 200, res.text
    data = res.json()

    assert "months_remaining" in data
    assert "required_monthly_saving" in data
    assert "avg_monthly_net_saving" in data
    assert "feasible" in data
    assert "suggested_cut_targets" in data
    assert isinstance(data["suggested_cut_targets"], list)
