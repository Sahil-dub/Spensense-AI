# Spensense AI

**Full-stack personal finance analytics platform for tracking transactions, understanding spending behavior, and planning savings goals.**

Built with **FastAPI, PostgreSQL, Next.js, TypeScript, Recharts, Docker, and Python**.

> **Note:** Despite the project name, the current intelligence layer is rule-based. ML classification, prediction, and anomaly detection are planned extensions rather than implemented features.

> **Live recruiter demo:** GitHub Pages static showcase with representative dashboard data. The production application remains the FastAPI + PostgreSQL + Next.js stack described below.

## Project at a glance

| Area | Implementation |
|---|---|
| Transaction management | Income, expenses, editing, deletion |
| Data ingestion | CSV import |
| Financial analytics | Spending, savings, categories, trends |
| Expense intelligence | Rule-based Necessary / Controllable / Unnecessary classification |
| Planning | Savings goals + feasibility estimation |
| Backend | FastAPI + SQLAlchemy |
| Database | PostgreSQL |
| Frontend | Next.js + React + TypeScript |
| Visualization | Recharts |
| Migrations | Alembic |
| Testing | pytest |
| Infrastructure | Docker Compose |

## What it does

Spensense turns transaction data into a structured financial analytics workflow.

A user can:

- Record and manage income and expenses.
- Import transactions from CSV files.
- Categorize spending.
- Classify expenses into **Necessary, Controllable, or Unnecessary** buckets.
- Analyze spending over a selected date range.
- Track savings as a running balance.
- Identify daily spending spikes.
- Compare expense and savings views.
- Monitor category-level spending.
- Set spending thresholds and receive alerts.
- Create savings goals and estimate whether they are feasible from historical spending.

## Why this project is interesting

This is not just a CRUD expense tracker. It combines:

**transaction data → backend business logic → PostgreSQL → analytics APIs → interactive dashboard → financial planning**

The project demonstrates the kind of full-stack data workflow useful for Data Analyst, BI, Data Engineering, and backend-oriented roles.

## Architecture

```mermaid
flowchart LR
    A["CSV / User Transactions"] --> B["Next.js Dashboard"]
    B --> C["FastAPI API"]
    C --> D["Business Logic"]
    D --> E["PostgreSQL"]
    D --> F["Financial Analytics"]
    F --> B
```

## Analytics & intelligence

### Spending analytics

- Daily expense trend and spike detection.
- Running savings balance.
- Expense vs savings views.
- Category-level income and expense analysis.
- Configurable spending thresholds.

### Expense classification

The current system applies rule-based logic to classify expenses into:

- **Necessary**
- **Controllable**
- **Unnecessary**

The architecture is intentionally separated so that a future ML classifier can replace or complement the current rules.

### Savings planning

Users can define a savings target and receive:

- Required monthly savings.
- Estimated timeline.
- Feasibility based on historical spending behavior.

## Backend engineering

The FastAPI backend is structured into separate layers for:

- API routes
- Pydantic schemas
- SQLAlchemy models
- CRUD/database operations
- Business services
- Configuration and logging
- Database migrations

The API provides the application boundary between the dashboard and PostgreSQL while keeping financial calculations and business rules in backend services.

Swagger documentation is available locally at:

```text
http://localhost:8000/docs
```

## Frontend

The dashboard uses:

- Next.js
- React
- TypeScript
- Tailwind CSS
- Recharts
- next-themes

The UI supports:

- Interactive charts and tooltips.
- Date-range filtering.
- Expense/savings switching.
- Dark/light themes.
- Responsive layouts.

## Data flow

```text
User transaction / CSV
        ↓
    FastAPI API
        ↓
Validation + business logic
        ↓
    PostgreSQL
        ↓
Financial analytics services
        ↓
    JSON responses
        ↓
 Next.js dashboard
```

## Tech stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- pytest
- Ruff
- Black

### Frontend
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Recharts
- next-themes

### Infrastructure
- Docker
- Docker Compose

## Repository structure

```text
Spensense-AI/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── crud/         # Database operations
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic and analytics
│   │   └── core/         # Configuration and logging
│   ├── tests/            # Backend tests
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/components/   # Dashboard and visualization components
│   ├── Dockerfile
│   └── .env.local.example
├── docker-compose.yml
└── README.md
```

## Run locally

### Docker — recommended

Requirements:

- Docker Desktop / Docker Engine

Start the complete stack:

```bash
docker compose up --build
```

Open:

```text
Frontend:    http://localhost:3000
Backend API: http://localhost:8000
Swagger:     http://localhost:8000/docs
```

Stop:

```bash
docker compose down
```

Reset the database:

```bash
docker compose down -v
```

### Manual setup

Requirements:

- Python 3.11+
- Node.js 22+
- PostgreSQL 16+

Backend:

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -U pip
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## Environment variables

### Backend

Create `backend/.env` from `backend/.env.example`:

```env
APP_NAME=Spensense AI API
ENVIRONMENT=local
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
DATABASE_URL=postgresql+psycopg://spendsense:spendsense@localhost:5432/spendsense
```

### Frontend

Create `frontend/.env.local` from `frontend/.env.local.example`:

```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

Local environment files are intentionally git-ignored.

## Testing & code quality

Backend tests:

```bash
cd backend
pytest -q
```

Lint:

```bash
ruff check .
```

Format:

```bash
black .
```

The backend is configured with Ruff rules covering common Python errors, imports, and bug-prone patterns.

## Roadmap

The next engineering extensions are:

- [ ] JWT authentication
- [ ] Multi-user support
- [ ] Multi-currency transactions
- [ ] ML-based expense classification
- [ ] Spending prediction
- [ ] Anomaly detection
- [ ] CI/CD automation
- [ ] Free cloud deployment

The roadmap is intentionally separate from the current feature set so implemented functionality is not confused with planned work.

## Project positioning

Spensense demonstrates a broader workflow than a typical beginner dashboard:

**Full-stack application → relational data → APIs → financial business logic → analytics → visualization**

It is particularly useful as a portfolio example for roles involving **Python, SQL, APIs, PostgreSQL, analytics, and data-driven application development**.

## Author

**Sahil Dubey**  
M.Sc. Data Science student in Germany

