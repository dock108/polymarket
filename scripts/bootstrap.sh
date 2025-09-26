#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"

echo "[bootstrap] Repo root: $ROOT_DIR"

# Python venv hint (not enforced)
echo "[bootstrap] Tip: Create a Python 3.11 venv for backend development"
echo "[bootstrap]   python3.11 -m venv .venv && source .venv/bin/activate"

# Create local env example if missing
if [ ! -f "$ROOT_DIR/.env.example" ]; then
  cat > "$ROOT_DIR/.env.example" <<'EOF'
# Example environment file
DATABASE_URL=sqlite:///./data/dev.db
ODDS_API_KEY=
DATAGOLF_API_KEY=
FEE_CUSHION=0.025
REFRESH_INTERVAL_SECONDS=600
EOF
  echo "[bootstrap] Wrote .env.example"
fi

mkdir -p "$ROOT_DIR/data"
echo "[bootstrap] Created data directory (for dev SQLite)"

echo "[bootstrap] Done. See README.md and issues/ for next steps."
