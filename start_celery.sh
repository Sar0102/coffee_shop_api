#!/usr/bin/env bash
set -euo pipefail

CELERY_APP="${CELERY_APP:-src.infrastructure.tasks.celery_app:celery}"
LOG_LEVEL="${CELERY_LOG_LEVEL:-INFO}"
POOL="${CELERY_POOL:-solo}"

echo "[entrypoint-celery] Starting Celery worker & beat..."

celery -A "$CELERY_APP" worker \
  --loglevel="$LOG_LEVEL" \
  --pool="${POOL}" &
WORKER_PID=$!

celery -A "$CELERY_APP" beat \
  --loglevel="$LOG_LEVEL" \
  --pidfile= \
  --scheduler celery.beat:PersistentScheduler &
BEAT_PID=$!

trap "echo 'Stopping...'; kill -TERM $WORKER_PID $BEAT_PID; wait" SIGINT SIGTERM

wait -n $WORKER_PID $BEAT_PID
