FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir poetry
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml poetry.lock* ./

RUN poetry install --only=main --no-interaction --no-ansi --no-root

COPY . .

ENV PYTHONPATH=/app

RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

CMD ["python3", "-m", "src.adapters.workers.sync_telegram_gifts"]