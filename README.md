# Polymarket Sports Betting Edge App

Monorepo for a FastAPI backend and SwiftUI iOS app that surfaces positive-EV opportunities by aggregating Polymarket markets, sharp sportsbook lines, and DataGolf forecasts.

## Architecture at a Glance
- Backend: FastAPI (Python 3.11+), SQLAlchemy, Pydantic, httpx; Dockerized; Nginx reverse proxy in prod.
- Frontend: SwiftUI (iOS 17+), async/await `URLSession`, Codable DTOs.
- Data Sources: Polymarket Gamma API (binary markets), The Odds API v4, DataGolf.
- Conventions: fee cushion on Polymarket, vig removal for books, unified EV/edge.

## Repo Layout
- `/backend` – FastAPI app (services, API, DB models, utils)
- `/frontend` – SwiftUI iOS app
- `/docs` – docs and runbooks
- `/issues` – standardized issue markdowns

## Quickstart (Dev)
1. Ensure Python 3.11+ and Xcode (for iOS) are installed.
2. Run `scripts/bootstrap.sh` (creates local env stubs and tips).
3. See `issues/` for the active tasks. Start with 092625-2..5.

## Guidelines
- See `AGENTS.md` for collaboration rules and Definition of Done.
- Do not commit real secrets. Use `.env` locally and GitHub secrets in CI.

## Status
Initial scaffolding; see `issues/092625-1.md` for checklist.
