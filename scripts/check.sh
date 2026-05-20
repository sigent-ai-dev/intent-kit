#!/usr/bin/env bash
set -euo pipefail

# Intent Kit — CI wrapper for intent check
# Usage: ./scripts/check.sh [--verbose] [--fix]
# Exit codes: 0 = pass, 1 = fail

ARGS=()
for arg in "$@"; do
    ARGS+=("$arg")
done

if command -v intent &>/dev/null; then
    intent check "${ARGS[@]}"
elif command -v uv &>/dev/null; then
    uv run intent check "${ARGS[@]}"
else
    echo "Error: neither 'intent' nor 'uv' found on PATH" >&2
    exit 1
fi
