#!/bin/sh
set -e

# Production entrypoint script
# Handles database migrations and starts the application server

# Ensure we're using the virtual environment's Python
PYTHON="${PYTHON:-/usr/src/app/.venv/bin/python}"

# Verify virtual environment is accessible
if [ ! -f "$PYTHON" ]; then
    echo "ERROR: Virtual environment Python not found at $PYTHON"
    echo "PATH: $PATH"
    which python || echo "python not found in PATH"
    exit 1
fi

# Wait for database to be ready
if [ -n "${DB_WAIT_SECONDS:-}" ]; then
    echo "Waiting for database... (${DB_WAIT_SECONDS}s)"
    sleep "${DB_WAIT_SECONDS}"
fi

# Apply database migrations (idempotent)
echo "Applying database migrations..."
"$PYTHON" manage.py migrate --noinput

# Collect static files if needed (for production)
if [ -n "${COLLECT_STATIC:-}" ] && [ "${COLLECT_STATIC}" != "0" ]; then
    echo "Collecting static files..."
    "$PYTHON" manage.py collectstatic --noinput --clear 2>/dev/null || echo "Static files collection skipped"
fi

# Start ASGI server (Gunicorn+Uvicorn)
# Using exec to replace shell process for proper signal handling
echo "Starting Gunicorn+Uvicorn (ASGI) on port ${PORT:-8001}..."
exec gunicorn --config docker/development/gunicorn.config.py config.asgi:application
