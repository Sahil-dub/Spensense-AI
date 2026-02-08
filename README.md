# Spensense AI 💸📊

Spensense AI is a full-stack expense tracking and financial insights platform built as a **portfolio-grade project** by a Master's student in Data Science.

The project focuses on making personal finances **visible, structured, and actionable** through clean backend design, interactive analytics, and intelligent categorization.

---

## 📋 Table of Contents

- [What Problem Does It Solve?](#what-problem-does-it-solve)
- [Features](#features)
- [Intelligence Layer](#intelligence-layer)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Environment Variables](#environment-variables)
- [Testing & Code Quality](#testing--code-quality)
- [Roadmap](#roadmap)
- [Author](#author)
- [License](#license)

---

## 🎯 What Problem Does It Solve?

Many people don't clearly understand:
- Where their money goes
- Which expenses are necessary vs controllable
- How much they are actually saving over time

Spensense AI helps users **track**, **analyze**, and **reflect** on their financial behavior using data-driven insights.

---

## ✨ Features

### Core Functionality
- Add, edit, and delete income and expense transactions
- CSV import for bulk transaction uploads
- Predefined categories with a custom "Other" option
- Automatic expense bucket classification:
  - Necessary
  - Controllable
  - Unnecessary

### Analytics & Visualization
- Daily expense spike chart
- Savings running-balance chart
- Toggle between Expense view and Savings view
- Shared date-range selector across all charts
- Category-wise income and expense pie charts
- Alerts when spending exceeds thresholds

### Goals & Planning
- Savings goal planner
- Feasibility estimation based on past spending
- Suggested timelines and required monthly savings

### User Experience
- Dark / light theme toggle
- Interactive charts with tooltips, zoom, and animations
- Responsive dashboard layout

---

## 🧠 Intelligence Layer

- Rule-based expense bucket inference
- Architecture designed to be extended with:
  - Machine learning classification
  - Spending prediction
  - Anomaly detection

---

## 🛠️ Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic (migrations)
- pytest, ruff, black

### Frontend
- Next.js (React)
- TypeScript
- Tailwind CSS
- Recharts
- next-themes

### Development & Tooling
- Docker & Docker Compose
- Git with clean commit history

---

## 📁 Project Structure

```
Spensense-AI/
│
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── crud/         # Database operations
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── core/         # Configuration & logging
│   ├── tests/
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/components/   # Dashboard and charts
│   ├── Dockerfile
│   └── .env.local.example
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Local Development

### Docker (Recommended)

**Requirements:**
- Docker Desktop (Windows / Mac) or Docker Engine (Linux)

**Start the full stack:**
```bash
docker compose up --build
```

**Open in browser:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

**Stop containers:**
```bash
docker compose down
```

**Reset database:**
```bash
docker compose down -v
```

### Manual Setup (Without Docker)

**Requirements:**
- Python 3.11+
- Node.js 22+
- PostgreSQL 16+

**Backend:**
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/Mac
pip install -U pip
pip install .
alembic upgrade head
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

### Backend (`backend/.env.example`)
```env
APP_NAME=Spensense AI API
ENVIRONMENT=local
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
DATABASE_URL=postgresql+psycopg://spendsense:spendsense@localhost:5432/spendsense
```

### Frontend (`frontend/.env.local.example`)
```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

> **Note:** Local `.env` files are intentionally git-ignored.

---

## 🧪 Testing & Code Quality

**Run backend tests:**
```bash
cd backend
pytest -q
```

**Lint and format:**
```bash
ruff check .
black .
```

---

## 🗺️ Roadmap

- [ ] Authentication (JWT)
- [ ] Multi-user support
- [ ] Multi-currency support
- [ ] ML-based expense classification
- [ ] CI/CD with GitHub Actions
- [ ] Free cloud deployment

---

## 👨‍💻 Author

**Sahil Dubey**  
Master's Student in Data Science (Germany)

This project was built to showcase practical backend engineering, data-driven thinking, and production-ready system design.

---

## 📄 License

Copyright (c) 2026 Sahil Dubey

---
