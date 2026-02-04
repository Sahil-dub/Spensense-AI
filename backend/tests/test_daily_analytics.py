from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_daily_analytics_points():
    today = date.today()
    d1 = today - timedelta(days=2)
    d2 = today - timedelta(days=1)

    # Seed transactions
    client.post(
        "/transactions",
        json={
            "tx_type": "income",
            "amount": 100,
            "currency": "EUR",
            "category": "salary",
            "bucket": None,
            "occurred_on": str(d1),
            "note": "seed",
        },
    )
    client.post(
        "/transactions",
        json={
            "tx_type": "expense",
            "amount": 40,
            "currency": "EUR",
            "category": "dining_out",
            "bucket": None,
            "occurred_on": str(d1),
            "note": "seed",
        },
    )
    client.post(
        "/transactions",
        json={
            "tx_type": "expense",
            "amount": 10,
            "currency": "EUR",
            "category": "shopping",
            "bucket": None,
            "occurred_on": str(d2),
            "note": "seed",
        },
    )

    res = client.get(f"/analytics/daily?date_from={d1}&date_to={today}")
    assert res.status_code == 200, res.text

    data = res.json()
    assert "points" in data
    assert isinstance(data["points"], list)
    assert any(p["date"] == str(d1) for p in data["points"])
