from __future__ import annotations

import io
from dataclasses import dataclass
from datetime import date

import pandas as pd
import pandera as pa
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.services.csv_schema import TRANSACTION_CSV_SCHEMA


@dataclass
class RejectRow:
    row_number: int  # 1-based for user friendliness (excluding header)
    reason: str


@dataclass
class ImportResult:
    inserted_count: int
    rejected_rows: list[RejectRow]


def _normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names: trim + lowercase
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Ensure optional columns exist
    for col in ["currency", "category", "bucket", "note"]:
        if col not in df.columns:
            df[col] = None

    # Default currency if blank
    df["currency"] = df["currency"].fillna("EUR")
    df["currency"] = df["currency"].replace("", "EUR")

    return df


def import_transactions_csv(db: Session, file_bytes: bytes) -> ImportResult:
    # Read CSV
    df = pd.read_csv(io.BytesIO(file_bytes))

    if df.empty:
        return ImportResult(inserted_count=0, rejected_rows=[RejectRow(1, "CSV is empty")])

    df = _normalize_dataframe(df)

    # Validate with pandera
    try:
        validated = TRANSACTION_CSV_SCHEMA.validate(df, lazy=True)
    except pa.errors.SchemaErrors as e:
        # Build rejected rows with reasons using failure_cases
        rejected: list[RejectRow] = []
        failure_cases = e.failure_cases

        # failure_cases contains row indices in "index"; these are 0-based data rows (not header)
        for _, row in failure_cases.iterrows():
            idx = int(row.get("index")) if row.get("index") is not None else 0
            col = str(row.get("column", "unknown"))
            check = str(row.get("check", "invalid"))
            failure = str(row.get("failure_case", ""))
            reason = f"{col}: {check} ({failure})".strip()
            rejected.append(RejectRow(row_number=idx + 1, reason=reason))

        # If validation fails, we can still try to insert the valid rows:
        # Get rows that passed by filtering out failed indices.
        failed_indices = set(int(i) for i in failure_cases["index"].dropna().unique())
        valid_df = df.drop(index=list(failed_indices), errors="ignore")

        if valid_df.empty:
            # Deduplicate reasons per row_number (keep first)
            seen = set()
            uniq = []
            for r in rejected:
                if r.row_number not in seen:
                    seen.add(r.row_number)
                    uniq.append(r)
            return ImportResult(inserted_count=0, rejected_rows=uniq)

        # Validate again but only on valid_df to coerce types cleanly
        validated = TRANSACTION_CSV_SCHEMA.validate(valid_df, lazy=False)

        # Deduplicate rejected per row
        seen = set()
        uniq = []
        for r in rejected:
            if r.row_number not in seen:
                seen.add(r.row_number)
                uniq.append(r)
        rejected = uniq
    else:
        rejected = []

    # Convert occurred_on to date
    validated["occurred_on"] = pd.to_datetime(validated["occurred_on"]).dt.date

    # Create SQLAlchemy objects
    txs: list[Transaction] = []
    for _, r in validated.iterrows():
        txs.append(
            Transaction(
                tx_type=str(r["tx_type"]),
                amount=r["amount"],  # SQLAlchemy Numeric will convert
                currency=str(r["currency"])[:3].upper() if r["currency"] else "EUR",
                category=(str(r["category"])[:50] if pd.notna(r["category"]) else None),
                bucket=(str(r["bucket"])[:20] if pd.notna(r["bucket"]) else None),
                occurred_on=r["occurred_on"],  # already date
                note=(str(r["note"])[:255] if pd.notna(r["note"]) else None),
            )
        )

    db.add_all(txs)
    db.commit()

    return ImportResult(inserted_count=len(txs), rejected_rows=rejected)
