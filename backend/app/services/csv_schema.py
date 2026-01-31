from __future__ import annotations

import pandera as pa
from pandera import Column
from pandera.dtypes import DateTime

# We validate "occurred_on" as datetime; later we convert to date
TRANSACTION_CSV_SCHEMA = pa.DataFrameSchema(
    {
        "tx_type": Column(
            pa.String,
            nullable=False,
            checks=pa.Check.isin(["income", "expense"]),
            coerce=True,
        ),
        "amount": Column(
            pa.Float,
            nullable=False,
            checks=pa.Check.gt(0),
            coerce=True,
        ),
        "currency": Column(
            pa.String,
            nullable=True,
            coerce=True,
            default="EUR",
        ),
        "category": Column(pa.String, nullable=True, coerce=True),
        "bucket": Column(
            pa.String,
            nullable=True,
            checks=pa.Check.isin(["necessary", "controllable", "unnecessary"]),
            coerce=True,
        ),
        "occurred_on": Column(DateTime, nullable=False, coerce=True),
        "note": Column(pa.String, nullable=True, coerce=True),
    },
    strict=False,  # allow extra columns, we just ignore them
)
