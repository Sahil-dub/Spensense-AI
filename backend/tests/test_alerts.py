from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_alerts_over_budget():
    # Create budget for dining_out = 30 EUR
    res_b = client.post(
        "/budgets",
        json={"category": "dining_out", "monthly_limit": 30, "currency": "EUR"},
    )
    assert res_b.status_code in (201, 409), res_b.text  # allow if already exists from earlier tests

    # Add expenses this month totaling 45
    today = str(date.today())
    payloads = [
        {
            "tx_type": "expense",
            "amount": 20,
            "currency": "EUR",
            "category": "dining_out",
            "bucket": "controllable",
            "occurred_on": today,
        },
        {
            "tx_type": "expense",
            "amount": 25,
            "currency": "EUR",
            "category": "dining_out",
            "bucket": "controllable",
            "occurred_on": today,
        },
    ]
    for p in payloads:
        r = client.post("/transactions", json=p)
        assert r.status_code == 201, r.text

    res = client.get("/alerts")
    assert res.status_code == 200, res.text
    data = res.json()

    assert "alerts" in data
    # should include dining_out as over budget
    # (may include other alerts depending on prior test data)
    assert any(a["category"] == "dining_out" and float(a["over_by"]) >= 15 for a in data["alerts"])
