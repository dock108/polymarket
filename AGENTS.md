# AGENTS.md

Guidelines for AI coding assistants and developers collaborating on the Polymarket Sports Betting Edge App. These rules operationalize our development values and project context so contributors can execute quickly and consistently.

---

## Core Principles

1) Persistence & Completion
- Never give up; work until 100% complete or a genuine showstopper.
- If blocked, try alternate approaches; document the blocker succinctly.
- “Done” means: code runs, tests pass, feature works, and is ready for user testing.
- Keep issues open in "Awaiting User Testing" until the user explicitly confirms completion.

2) User First
- Prioritize the most recent user request and scope.
- Don’t add unrequested features or scope creep.
- Deliver working, minimal, and complete increments.

3) Keep It Simple
- Prefer simple, readable implementations.
- Match existing patterns. Avoid unnecessary dependencies.

4) Ask When Unclear
- Interrupt only for critical blockers or missing inputs (e.g., secrets, domain, API keys).
- Otherwise proceed with sensible defaults and note assumptions.

5) Fail Loudly, Not Defensively
- No catch-all or speculative error handling. Fail fast with clear messages.
- Only handle errors that can be meaningfully recovered from.

---

## Project Context (Essentials)

- Monorepo layout: `/backend` (FastAPI, Python 3.11+), `/frontend` (SwiftUI, iOS 17+), `/docs`, `issues/`.
- Backend: FastAPI (ASGI), httpx/requests, SQLAlchemy, Pydantic. SQLite for dev, plan for Postgres in prod (Alembic migrations). Dockerized with Uvicorn/Gunicorn; Nginx reverse proxy; deploy on Hetzner with HTTPS (Let’s Encrypt).
- Frontend: SwiftUI (iOS 17+). Tabs: All Sports, Golf (DataGolf), Settings. Networking with async/await (`URLSession`), Codable models.
- External data sources:
  - Polymarket Gamma API (public endpoints). Use sports/events/markets; binary markets only.
  - The Odds API v4 (bookmakers: Pinnacle, Betfair, Caesars, Circa, Bookmaker.eu).
  - DataGolf API (schedule + pre-tournament win probabilities).
- Caching & polling: cache responses (5–10 min TTL); poll external APIs at most every ~10 minutes.
- Odds modeling: implied probability; remove sportsbook vig; apply Polymarket fee cushion (2.5–3% configurable). Compute fair odds, edge%, EV.

---

## Definition of Done (DoD)

A task/issue is ready for user testing only when all apply:
- Code compiles/builds; app runs locally (and in container when relevant).
- Tests exist for core logic and pass (backend ~80% coverage target for critical modules).
- Linters/formatters pass (Python: black/flake8; iOS: Xcode build clean).
- API/UX behavior documented in the issue "Testing Requirements" section.
- "User Confirmation & Actions Required" is documented in the issue and addressed where possible.
- Issue status set to "Awaiting User Testing" and remains open until the user confirms.

---

## Issues & Workflow

- Issues live under `issues/*.md` following `STANDARDIZED_ISSUE_TEMPLATE.md`.
- Name format: `MMDDYY-N`. Keep titles concise; one clear outcome per issue.
- Always include: Problem, Investigation Areas, Expected Behavior, Files to Investigate, Solution, Code Changes, Testing Requirements, Status, Implementation Checklist, Completion Criteria, User Testing Confirmation, User Confirmation & Actions Required, Result.
- Each issue must include a user-facing confirmation section (env vars to set, keys to provide, domain/DNS, etc.).
- Don’t move issues to done/complete folders until user testing is confirmed by the user.

---

## Backend Execution Rules

- Services: encapsulate each data source (`PolymarketService`, `OddsService`, `DataGolfService`) and an aggregation layer for opportunities.
- Endpoints (public):
  - `GET /api/opportunities` – aggregated list (sortable/filterable, paginated)
  - `GET /api/odds/{sport}` – raw/normalized odds
  - `GET /api/golf` – DG +EV golf bets
- DB & Migrations: SQLAlchemy models; Alembic migrations from the start (SQLite dev -> Postgres ready).
- Caching & Rate Limits: use fastapi-cache or service-level memoization with TTL; respect upstream limits.
- HTTP Clients: timeouts, bounded retries with backoff; structured logging of request/response metadata (no secrets).
- Error Handling: map upstream failures to 503; include clear error payloads; log context.
- Odds/EV utilities: centralize conversions, vig removal, EV and edge% computations with unit tests.

---

## Frontend Execution Rules

- Tabs and views:
  - All Sports: list opportunities sorted by EV%, filters (sport, EV threshold), loading/empty/error states.
  - Golf: list DG +EV items with toggle to show only +EV; show DG prob, best odds, EV%.
  - Detail View: show sportsbook lines, Polymarket odds, fair odds, edge%, EV, freshness.
  - Settings: fee cushion slider, refresh interval, default EV threshold, Developer Mode toggle.
- Networking: async/await, Codable DTOs; configurable base URL for dev/prod; simple retry for transient failures.
- UX: fast, legible defaults; numeric formatting consistent with backend outputs.

---

## Configuration & Secrets

- `.env.example` documents required and optional env vars.
- Required (examples):
  - `ODDS_API_KEY` – The Odds API v4 key
  - `DATAGOLF_API_KEY` – DataGolf API key
  - `DATABASE_URL` – SQLite path in dev; Postgres in prod
  - `FEE_CUSHION` – decimal (e.g., `0.025`)
  - `REFRESH_INTERVAL_SECONDS` – e.g., `600`
- Never commit real secrets. Use GitHub secrets for CI/CD as needed.

---

## Testing, CI/CD, and Quality Gates

- Backend tests with `pytest`; include unit and integration tests for services and utilities.
- Lint/format with black/flake8; enforce in CI.
- CI (GitHub Actions): run lint/tests on PRs; build container on main; surface coverage summary.
- iOS minimal CI: build target and run unit tests if present (no signing required).

---

## Deployment Overview

- Containerized FastAPI behind Nginx reverse proxy on Hetzner VPS.
- HTTPS via Let’s Encrypt; health checks exposed; logs rotated.
- Release pipeline builds/tags/pushes images and updates the stack (compose or Kamal).
- Keep a rollback path (previous tag).

---

## Data & Modeling Conventions

- Polymarket binary markets only; map outcomes consistently (Yes/No).
- Implied probability and fee application: `true_prob = implied_prob * (1 - fee)`; clamp to [0,1].
- Vig removal for two-outcome books: scale implied probs to sum to 1; compute fair odds.
- EV (for $1 stake): `EV = P_true * (odds - 1) - (1 - P_true) * 1`.
- Always log calculation inputs and outputs sufficiently for debugging (no secrets).

---

## Communication & Status Updates

- Provide brief status updates in PRs/issues: what changed, what’s next, any risks.
- If you say you are about to do something, execute in the same work unit when feasible.
- Keep updates concise and high-signal; link to relevant code and issues.

---

## What To Ask the User (Common)

- Missing secrets/keys (`ODDS_API_KEY`, `DATAGOLF_API_KEY`).
- Domain and DNS for HTTPS setup; preferred TLS settings.
- Default fee cushion, EV threshold, refresh interval.
- Bookmakers to include and target sports list.
- Retention policies for logs/snapshots; alert channels (Slack/Discord).

---

## Versioning

- Keep this document updated when processes or architecture change.
- Last Updated: 2025-09-26
