from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_bucket_autofill_on_expense_create():
    payload = {
        "tx_type": "expense",
        "amount": 12.5,
        "currency": "EUR",
        "category": "dining_out",
        "bucket": None,
        "occurred_on": str(date.today()),
        "note": "Burger",
    }
    res = client.post("/transactions", json=payload)
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["bucket"] == "controllable"


def test_bucket_not_set_for_income():
    payload = {
        "tx_type": "income",
        "amount": 100,
        "currency": "EUR",
        "category": "salary",
        "bucket": None,
        "occurred_on": str(date.today()),
        "note": "Pay",
    }
    res = client.post("/transactions", json=payload)
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["bucket"] is None
