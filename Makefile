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
