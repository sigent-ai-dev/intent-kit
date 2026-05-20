#!/usr/bin/env bash
set -euo pipefail

# Intent Kit — CI wrapper for intent init
# Usage: ./scripts/init.sh <project-name> [--ai agent] [--force]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <project-name> [--ai agent] [--force]" >&2
    exit 1
fi

ARGS=("$@")

if command -v intent &>/dev/null; then
    intent init "${ARGS[@]}"
elif command -v uv &>/dev/null; then
    uv run intent init "${ARGS[@]}"
else
    echo "Error: neither 'intent' nor 'uv' found on PATH" >&2
    exit 1
fi
