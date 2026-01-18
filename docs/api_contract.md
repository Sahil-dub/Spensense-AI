# API Contract (Draft)

Base URL (local): `http://localhost:8000`

## Transactions
### GET /transactions
Query: `limit`, `offset`, `from`, `to`, `tx_type`, `category`, `bucket`
Returns: list of transactions

### POST /transactions
Body:
- tx_type: "income" | "expense"
- amount: number
- currency: "EUR" (MVP)
- category: string (optional; can be auto-assigned later)
- bucket: "necessary" | "controllable" | "unnecessary" (optional; can be auto-assigned)
- occurred_on: YYYY-MM-DD
- note: string (optional)

### PUT /transactions/{id}
Updates fields above.

### DELETE /transactions/{id}
Deletes transaction.

## Import
### POST /import/csv
Upload a CSV file and return:
- inserted_count
- rejected_rows + reasons

## Analytics
### GET /analytics/summary
Returns:
- totals by month
- totals by category
- totals by bucket
- income vs expense
