#!/usr/bin/env bash
set -euo pipefail

# --- Config (env overrides allowed) ---
APP_IMPORT_PATH="${APP_IMPORT_PATH:-src.main:app}"
HOST="${SERVER_HOST:-0.0.0.0}"
PORT="${SERVER_PORT:-8000}"
WORKERS="${SERVER_WORKERS:-4}"
TIMEOUT="${SERVER_TIMEOUT:-60}"
GRACEFUL_TIMEOUT="${SERVER_GRACEFUL_TIMEOUT:-30}"
KEEP_ALIVE="${SERVER_KEEP_ALIVE:-5}"
LOG_LEVEL="${SERVER_LOG_LEVEL:-info}"

echo "[entrypoint] Running DB migrations..."
# Retry loop in case DB isn't ready yet
MAX_TRIES="${MIGRATION_MAX_TRIES:-30}"
SLEEP_SEC="${MIGRATION_SLEEP_SEC:-2}"

attempt=1
until alembic upgrade head; do
  if [ "$attempt" -ge "$MAX_TRIES" ]; then
    echo "[entrypoint] Migrations failed after ${MAX_TRIES} attempts. Exiting."
    exit 1
  fi
  echo "[entrypoint] alembic upgrade failed (attempt $attempt). Retrying in ${SLEEP_SEC}s..."
  attempt=$((attempt+1))
  sleep "$SLEEP_SEC"
done
echo "[entrypoint] Migrations applied."

echo "[entrypoint] Starting Gunicorn (${WORKERS} workers) ..."
exec gunicorn "${APP_IMPORT_PATH}" \
  --worker-class uvicorn.workers.UvicornWorker \
  --workers "${WORKERS}" \
  --bind "${HOST}:${PORT}" \
  --timeout "${TIMEOUT}" \
  --graceful-timeout "${GRACEFUL_TIMEOUT}" \
  --keep-alive "${KEEP_ALIVE}" \
  --log-level "${LOG_LEVEL}" \
  --access-logfile "-" \
  --error-logfile "-"
