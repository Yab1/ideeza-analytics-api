# ==============================================================================
# Project Setup
# ==============================================================================

PROJECT_NAME := ideeza-analytics-api
PYTHON       := uv run python
MANAGE       := $(PYTHON) manage.py
DJANGO_PORT  := 8000
COLOR_RESET  := \033[0m
COLOR_BLUE   := \033[1;34m
COLOR_GREEN  := \033[1;32m
COLOR_YELLOW := \033[1;33m

define title
	@echo "$(COLOR_BLUE)==>$(COLOR_RESET) $(1)"
endef

define ok
	@echo "$(COLOR_GREEN)✔$(COLOR_RESET) $(1)"
endef

# ==============================================================================
# Help
# ==============================================================================
.PHONY: help
help:
	@echo ""
	@echo "$(COLOR_YELLOW)Available commands:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-25s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""

# ==============================================================================
# Environment
# ==============================================================================
.PHONY: install precommit update

install: ## Install all dependencies (dev + prod) using uv
	$(call title,Installing all dependencies with uv)
	@bash ./scripts/install.sh
	$(call ok,Dependencies installed)

precommit: ## Install and configure pre-commit hooks
	$(call title,Setting up pre-commit)
	uv run pre-commit uninstall || true
	uv run pre-commit install
	$(call ok,Pre-commit hooks installed)

# ==============================================================================
# Django Management
# ==============================================================================
.PHONY: run migrate makemigrate dry-migrate shell superuser seed-superuser collectstatic flush seed-patients django-check migrations

# ==============================================================================
# Server & Development
# ==============================================================================
run: ## Run Django server
	$(call title,Running server on DJANGO_PORT $(DJANGO_PORT))
	$(MANAGE) runserver $(DJANGO_PORT)

shell: ## Open Django shell
	$(MANAGE) shell

django-check: ## Check Django health and perform checks
	$(MANAGE) check

# ==============================================================================
# Migrations
# ==============================================================================
migrations: ## Create migrations
	$(MANAGE) makemigrations

migrate: ## Apply migrations
	$(MANAGE) migrate

makemigrate: ## Create and apply migrations
	$(MANAGE) makemigrations
	$(MANAGE) migrate

dry-migrate: ## Dry run migrations
	$(MANAGE) makemigrations --dry-run 2>&1 | head -20

# ==============================================================================
# User Management
# ==============================================================================
superuser: ## Create superuser
	$(MANAGE) createsuperuser

seed-superuser: ## Load superusers from YAML secrets file (use --update to update existing)
	$(call title,Loading superusers from secrets file)
	$(MANAGE) load_superusers $(if $(UPDATE),--update,)

# ==============================================================================
# Static Files
# ==============================================================================
collectstatic: ## Collect static files
	$(MANAGE) collectstatic --noinput


# ==============================================================================
# Miscellaneous
# ==============================================================================
.PHONY: clean-migrations format lint demo-logging create-app loaddata loaddata-all

clean-migrations: ## Remove migration files
	find core -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find core -path "*/migrations/*.pyc" -delete
	$(call ok,Migrations cleaned)

format: ## Format code with ruff
	$(call title,Formatting code)
	uv run ruff format .
	$(call ok,Code formatted)

lint: format ## Run linters (includes formatting)
	$(call title,Running linters)
	@echo "Running ruff check on all Python files..."
	uv run ruff check . --fix
	@echo "Running other pre-commit hooks..."
	uv run pre-commit run --all-files check-yaml
	uv run pre-commit run --all-files check-added-large-files
	$(call ok,Linting complete)

load-fixtures: ## Load all fixtures
	$(MANAGE) loaddata $(shell find core -type f -path "*/fixtures/*" \( -name '*.json' -o -name '*.yaml' \))

# ==============================================================================
# Docker Orchestration
# ==============================================================================
.PHONY: docker docker-up docker-down docker-restart docker-ps docker-deploy

docker: ## Start Docker stack (ENV=local|production, default: production)
	@./scripts/docker-orchestrate.sh $(ENV)

docker-up: ## Start Docker stack (ENV=local|production, default: production)
	@./scripts/docker-orchestrate.sh $(ENV)

docker-down: ## Stop Docker stack (ENV=local|production, default: production)
	@./scripts/docker-orchestrate.sh $(ENV) down

docker-restart: ## Restart Docker stack (ENV=local|production, default: production)
	@./scripts/docker-orchestrate.sh $(ENV) restart

docker-ps: ## Show Docker stack status (ENV=local|production, default: production)
	@./scripts/docker-orchestrate.sh $(ENV) ps

docker-deploy: ## Deploy with Jenkins-style env handling (ENV=local|production, default: production)
	@./scripts/docker-orchestrate.sh $(ENV) deploy

