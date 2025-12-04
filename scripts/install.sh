#!/bin/bash

# Ensure uv is in PATH
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

# Check if uv exists, install if not
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

# Sync dependencies (includes dev dependencies)
uv sync --extra dev
