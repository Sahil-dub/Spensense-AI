from datetime import date
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _seed_transactions():
    # Add a few transactions via API so analytics has data
    today = str(date.today())
    payloads = [
        {
            "tx_type": "income",
            "amount": 1000,
            "currency": "EUR",
            "category": "salary",
            "bucket": None,
            "occurred_on": today,
            "note": "seed income",
        },
        {
            "tx_type": "expense",
            "amount": 100,
            "currency": "EUR",
            "category": "rent",
            "bucket": "necessary",
            "occurred_on": today,
            "note": "seed rent",
        },
        {
            "tx_type": "expense",
            "amount": 25,
            "currency": "EUR",
            "category": "dining_out",
            "bucket": "controllable",
            "occurred_on": today,
            "note": "seed food",
        },
    ]
    for p in payloads:
        res = client.post("/transactions", json=p)
        assert res.status_code == 201, res.text


def test_analytics_summary_shape():
    _seed_transactions()
    res = client.get("/analytics/summary?top_categories=5&months=3")
    assert res.status_code == 200, res.text
    data = res.json()

    assert "totals" in data
    assert "by_bucket" in data
    assert "by_category" in data
    assert "monthly" in data

    assert Decimal(data["totals"]["income"]) >= Decimal("0")
    assert Decimal(data["totals"]["expense"]) >= Decimal("0")
    assert Decimal(data["totals"]["net"]) == Decimal(data["totals"]["income"]) - Decimal(
        data["totals"]["expense"]
    )
    assert isinstance(data["by_category"], list)
    assert isinstance(data["monthly"], list)
