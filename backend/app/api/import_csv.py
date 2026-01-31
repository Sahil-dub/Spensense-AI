from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.csv_import import import_transactions_csv

router = APIRouter(prefix="/import", tags=["import"])


@router.post("/csv")
async def import_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    result = import_transactions_csv(db, content)

    return {
        "inserted_count": result.inserted_count,
        "rejected_rows": [
            {"row_number": r.row_number, "reason": r.reason} for r in result.rejected_rows
        ],
    }
