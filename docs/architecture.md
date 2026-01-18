# Architecture (Phase 0)

## Goals
- Simple web app first, then ML/AI.
- Clear separation: UI (frontend), API (backend), DB (Postgres).

## High-level design
- Frontend: Next.js (TypeScript)
- Backend: FastAPI (Python)
- Database: PostgreSQL (Supabase hosted later)

## Data flow
1. User adds transaction (manual form or CSV upload)
2. Frontend calls backend API
3. Backend validates, classifies (rules first), stores in Postgres
4. Frontend fetches analytics summaries and renders charts

## MVP scope (Phase 1–2)
- Transactions CRUD
- CSV import
- Basic classification (rules)
- Analytics endpoints
- Dashboard charts

## Later scope
- Goal planning (feasibility + timeline)
- ML classification (TF-IDF + linear model)
- Auth + multi-user + multi-currency
