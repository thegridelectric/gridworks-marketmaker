#!/bin/bash
# Run locally everything CI runs, so a push won't go red. Mirrors
# .github/workflows/tests.yml. Usage: ./ci.sh
#
# The broker test needs GWMM_TEST_RABBIT_URL (the dev broker's d1__1
# vhost); it self-skips without one, so set it here to run the full gate.
set -euo pipefail

step() { printf '\n=== %s ===\n' "$1"; shift; "$@"; }

step "uv sync (locked)" uv sync --all-groups --locked
step "ruff check" uv run ruff check --no-fix .
step "ruff format --check" uv run ruff format --check .
step "pyright" uv run pyright
step "tests" uv run pytest -q

printf '\nAll CI checks passed.\n'
