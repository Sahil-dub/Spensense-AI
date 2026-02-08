FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -U pip && pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

EXPOSE 8000

# Run migrations + start API
CMD ["bash", "-lc", "python -m alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
