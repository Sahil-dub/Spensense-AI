from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_import_csv_inserts_and_rejects():
    csv_bytes = b"""tx_type,amount,currency,category,bucket,occurred_on,note
expense,12.50,EUR,dining_out,controllable,2026-01-25,Burger
expense,-5,EUR,shopping,unnecessary,2026-01-20,invalid amount
income,500,EUR,salary,,2026-01-01,monthly pay
"""
    files = {"file": ("sample.csv", csv_bytes, "text/csv")}
    res = client.post("/import/csv", files=files)
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["inserted_count"] == 2
    assert len(data["rejected_rows"]) >= 1


def test_import_csv_rejects_non_csv():
    files = {"file": ("sample.txt", b"hello", "text/plain")}
    res = client.post("/import/csv", files=files)
    assert res.status_code == 400
