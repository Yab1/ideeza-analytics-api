# Gunicorn configuration for Django + Uvicorn ASGI (Production)

# Server socket
bind = "0.0.0.0:8001"
backlog = 1024

# Worker processes
import multiprocessing  # noqa: E402

workers = (multiprocessing.cpu_count() * 2) + 1  # Recommended formula
# For development, you can set explicitly: workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 500
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Timeout settings
timeout = 60
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "analytics_api_gunicorn_dev"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
worker_tmp_dir = "/tmp"

# Memory management
max_requests = 1000
max_requests_jitter = 100

# Environment
raw_env = [
    "DJANGO_SETTINGS_MODULE=config.django.base",
]

# Production settings
reload = False
