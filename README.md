# Polymarket Sports Betting Edge App

Monorepo for a FastAPI backend and SwiftUI iOS app that identifies +EV opportunities by combining Polymarket and sportsbook odds.

## Quickstart

Prereqs:
- Python 3.11+
- Xcode 15+ (iOS 17 SDK)
- Homebrew (optional for tools)

Clone and bootstrap:
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=.
# env vars
cp ../.env.example ../.env
```

Run API (dev):
```bash
cd backend
./dev.sh
# visit http://localhost:8000/health
```

Open iOS app:
- `cd frontend`
- `xcodegen generate` (if not already generated)
- Open `PolymarketEdge.xcodeproj` and run on iOS 17 simulator.

## Environment
See `.env.example` for:
- ODDS_API_KEY
- DATAGOLF_API_KEY (backlogged features)
- DATABASE_URL, FEE_CUSHION, REFRESH_INTERVAL_SECONDS

## Backend
- FastAPI app factory in `backend/app/main.py`
- Services: Polymarket, Odds API, Opportunity engine
- Endpoints:
  - `GET /api/opportunities`
  - `GET /api/odds/{sport}`
  - `GET /api/golf` (placeholder)

## iOS App
- SwiftUI tabs: All Sports, Golf (backlog), Settings
- Networking with async/await; configurable `API_BASE_URL` in `frontend/Info.plist`
- Settings: fee cushion, refresh interval, default EV threshold, Developer Mode

## Testing
```bash
cd backend
source .venv/bin/activate
pytest -q
```

## Deployment (overview)
- Run backend behind Nginx reverse proxy with HTTPS (see `docs/runbooks/deploy.md`)
- Health: `/health`

## Docs
- API: `docs/api.md`
- Runbooks: `docs/runbooks/local.md`, `docs/runbooks/deploy.md`
