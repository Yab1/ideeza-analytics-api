FROM python:3.12.4-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/root/.local/bin:/root/.cargo/bin:$PATH

# Install build dependencies (minimal - only curl for uv installation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /usr/src/app

# Copy dependency files (these change less frequently)
COPY pyproject.toml uv.lock* ./
COPY .env ./.env

# Install dependencies (inline the install.sh logic since uv is already installed)
RUN uv sync --extra dev

# Verify virtual environment was created and Django is installed
RUN test -d .venv && .venv/bin/python -c "import django; print(f'Django {django.__version__} installed')" || (echo "ERROR: Virtual environment or Django not found!" && exit 1)

# Runtime stage
FROM python:3.12.4-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/usr/src/app/.venv/bin:$PATH

# Create non-root user
RUN groupadd -g 1000 app && useradd -m -u 1000 -g app appuser

WORKDIR /usr/src/app

# Copy virtual environment from builder
COPY --from=builder --chown=appuser:app /usr/src/app/.venv /usr/src/app/.venv

# Verify venv exists before copying app source
RUN test -d /usr/src/app/.venv && echo "Virtual environment copied successfully" || (echo "ERROR: Virtual environment not found!" && exit 1)

# Copy application source (already includes submodules)
COPY --chown=appuser:app . .

# Verify venv still exists after copying source (should not be overwritten)
RUN test -d /usr/src/app/.venv && /usr/src/app/.venv/bin/python -c "import django; print(f'Django {django.__version__} verified')" || (echo "ERROR: Virtual environment corrupted after copying source!" && exit 1)

# Copy and set up entrypoint
COPY --chown=appuser:app docker/development/entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Create logs directory (chown only logs, not entire tree - COPY already set ownership)
RUN mkdir -p /usr/src/app/logs && chown appuser:app /usr/src/app/logs

USER appuser

CMD ["./entrypoint.sh"]
