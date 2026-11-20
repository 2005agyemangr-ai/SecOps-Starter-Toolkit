#!/usr/bin/env bash
set -euo pipefail

OUT_FILE="snapshot_$(date +%Y%m%d_%H%M%S).txt"

{
  echo "=== System Health Snapshot ==="
  echo "Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
  echo "Hostname:  $(hostname)"
  echo ""
  echo "--- Uptime & Load ---"
  uptime
  echo ""
  echo "--- Memory ---"
  free -h 2>/dev/null || true
  echo ""
  echo "--- Disk Usage ---"
  df -hP
  echo ""
  echo "--- Listening Sockets ---"
  if command -v ss >/dev/null 2>&1; then
    ss -tulnp 2>/dev/null || ss -tuln
  elif command -v netstat >/dev/null 2>&1; then
    netstat -tuln
  else
    echo "Neither ss nor netstat available."
  fi
} > "$OUT_FILE"

echo "Snapshot written to $OUT_FILE"
