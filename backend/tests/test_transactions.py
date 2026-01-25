from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_transaction():
    payload = {
        "tx_type": "expense",
        "amount": 10.25,
        "currency": "EUR",
        "category": "dining_out",
        "bucket": "controllable",
        "occurred_on": str(date.today()),
        "note": "Test",
    }
    res = client.post("/transactions", json=payload)
    assert res.status_code == 201, res.text
    data = res.json()
    assert data["tx_type"] == "expense"
    tx_id = data["id"]

    res2 = client.get(f"/transactions/{tx_id}")
    assert res2.status_code == 200
    assert res2.json()["id"] == tx_id


def test_list_transactions_limit_offset():
    res = client.get("/transactions?limit=5&offset=0")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) <= 5
