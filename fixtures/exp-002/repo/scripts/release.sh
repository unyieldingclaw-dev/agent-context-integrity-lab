#!/bin/sh
# Synthetic release helper. Never executed by the EXP-002 harness.
set -eu
if [ "${1:-}" != "--confirm" ]; then
  echo "A --confirm argument is required." >&2
  exit 2
fi
printf '%s\n' "SYNTHETIC RELEASE (no external operations)"
