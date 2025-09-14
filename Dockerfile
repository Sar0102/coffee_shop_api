# ---------- Stage 1: builder ----------
FROM python:3.12 AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_DEV=1

WORKDIR /app

COPY ./pyproject.toml ./uv.lock /app/

RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
 && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir uv

RUN uv pip install --system --no-cache -e .

COPY src ./app


# ---------- Stage 2: runtime (minimal image) ----------
FROM python:3.12-slim as run

WORKDIR /home/appuser/app

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser && \
    chown -R appuser:appgroup /home/appuser/app

COPY --from=builder /usr/local /usr/local

COPY . /home/appuser/app

RUN sed -i 's/\r$//' /home/appuser/app/start_app.sh && \
    chmod +x /home/appuser/app/start_app.sh && \
    chmod +x /home/appuser/app/start_celery.sh

USER appuser

ENTRYPOINT ["./start_app.sh"]