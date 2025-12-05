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

# Wait for database to be ready (depends_on ensures it's healthy, but add a small buffer)
echo "Waiting for database connection..."
sleep 2

# Verify database connection
echo "Verifying database connection..."
"$PYTHON" manage.py check --database default || {
    echo "ERROR: Database connection failed"
    exit 1
}

# Apply database migrations (idempotent)
echo "Applying database migrations..."
"$PYTHON" manage.py migrate --noinput

# Load fixtures in correct dependency order
echo "Loading fixtures..."
"$PYTHON" manage.py loaddata \
    core/analytics/fixtures/country/country \
    core/users/fixtures/user/baseuser \
    core/users/fixtures/user/user \
    core/analytics/fixtures/blog/blog \
    core/analytics/fixtures/blogview/blogview || echo "Fixtures loading skipped or already loaded"

# Collect static files if needed (for production)
if [ -n "${COLLECT_STATIC:-}" ] && [ "${COLLECT_STATIC}" != "0" ]; then
    echo "Collecting static files..."
    "$PYTHON" manage.py collectstatic --noinput --clear 2>/dev/null || echo "Static files collection skipped"
fi

# Start ASGI server (Gunicorn+Uvicorn)
# Using exec to replace shell process for proper signal handling
echo "Starting Gunicorn+Uvicorn (ASGI) on port ${PORT:-8001}..."
exec gunicorn --config gunicorn.config.py config.asgi:application
