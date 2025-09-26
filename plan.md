# Implementation Plan: Polymarket Sports Betting Edge App

## Architecture Overview
- **Monorepo Structure:** Organize the codebase with separate folders (e.g. `/backend`, `/frontend`, `/docs`). Use a monorepo so the FastAPI backend (Python) and SwiftUI frontend (iOS) live together. Include a `README`, CI/CD configs, and environment setup scripts in the root.  
- **Tech Stack:** Backend in FastAPI (Python 3.11+) with ASGI server (Uvicorn/Gunicorn). Frontend in SwiftUI (iOS 17+). Use Docker to containerize the backend; plan for a lightweight PostgreSQL instance (initially SQLite for dev) with schema migration (e.g. Alembic).  
- **Dev/Test Environment:** Start with SQLite for quick prototyping; design schemas and ORM (e.g. SQLAlchemy) so switching to Postgres in production is smooth. Use Pydantic models for data validation. Configure environment variables for secrets and DB URLs.  
- **Deployment (Hetzner):** Deploy backend on a Hetzner VPS. Use Docker Compose or a deployment tool (e.g. Kamal) to spin up FastAPI, a reverse proxy (Nginx), and the database. Set up domain/DNS and HTTPS (Let's Encrypt). Plan for autoscaling or VPS upgrades as needed.  
- **CI/CD and Testing:** Integrate GitHub Actions (or similar) for automated testing and linting. Write unit/integration tests (pytest) for backend logic (odds calculations, API clients). Use black/flake8 for Python formatting. Require code reviews and tests before merge.  

## Polymarket Integration
Polymarket’s Gamma API provides sports market data. First, call `/sports` to fetch sport metadata and associated tag IDs. Then query `/events?closed=false` (filtering by relevant sport tags) to retrieve all active event markets. For each event, fetch its `/markets` if needed. Only consider two-outcome (binary) markets. Parse each market’s outcomes (e.g. “Yes/No”) and the current token prices (USDC share prices). Convert the Polymarket price to an implied win probability (since a $1 winning outcome token represents 100% probability). Adjust these probabilities by subtracting Polymarket’s exchange fee (we assume ~2.5%, even though the official docs state no trade fees). Provide a tunable “fee cushion” parameter (e.g. 2.5–3%) in settings so the app’s EV calculations use post-fee odds.  

- Use Polymarket’s GraphQL or REST API (Gamma REST) and authenticate if needed (public endpoints require no auth).  
- Cache market data for a short time (e.g. 5–10 minutes) to avoid API rate limits.  
- Normalize Polymarket odds: calculate implied probability = share_price (decimal between 0 and 1), then `true_prob = implied_prob * (1 - fee)`. Compute the fair odds = 1 / true_prob for display.  

## Odds API Integration
Leverage a sportsbook odds API (e.g. The Odds API) to pull lines for all two-outcome bets (moneyline, point spreads, totals, alternate lines, binary props). Use the `/v4/sports/{sport}/odds` endpoint with appropriate parameters: set `regions=us` (or specific region codes) and `markets=h2h,spreads,totals,outrights` to include all relevant markets. Specify the five “sharp” sportsbooks via the `bookmakers` parameter (Pinnacle, Betfair Exchange, Caesars, Circa, Bookmaker.eu) by their keys. For each returned game with two sides (e.g. team A vs team B), record each bookmaker’s odds.  

- **Conservative Line Selection:** For each side of the bet, identify the shortest (most conservative) odds line across the five books (highest implied probability). E.g. if Book X offers +150 on Team A and Book Y offers +140 (implying 41.7% and 41.1%), take +140.  
- **Remove Vig:** Using the chosen book’s pair of odds, compute the implied probabilities and scale them to sum 100%. This back-out of the bookmaker’s margin (vig) yields “fair” probabilities. Convert those to fair odds.  
- **Refresh Schedule:** Poll this Odds API at most every 10 minutes (configurable). Log each API call with timestamp, request details, response status, and any errors. Store raw and normalized odds in the database for analysis.  

## DataGolf Integration (Golf Tab)
Integrate DataGolf’s API for golf forecasts. Use the `preds/pre-tournament` endpoint to retrieve probabilistic forecasts for upcoming golf tournaments. This returns, for each player in the field, their projected probabilities of various finish positions (win, top 5, etc.). Focus on the “win” probability. Compare DataGolf’s win probability (interpreted as `P_true`) against the odds implied by sportsbooks and Polymarket markets. Flag bets where DG’s probability implies positive EV (DG predicts a higher chance than the market).  

- Fetch the current PGA and other tour schedules (`get-schedule`) to determine current events.  
- Call DataGolf’s API with your API key to get the field projections.  
- For each golfer: if `P_DG_win * (odds payout) – (1 - P_DG_win) * stake > 0`, mark as +EV.  
- In the frontend “Golf” tab, include filters to show only DG+EV bets and to highlight mismatches. Label a bet (e.g. “DG+EV”) if DataGolf strongly disagrees with the line.  

## Odds Normalization Module
Implement a utility module to handle odds conversions and EV calculations. Key functions:  

- **Odds Conversion:** Convert between American and Decimal odds. For decimal odds d, implied probability p = 1/d. For American odds A: if A<0, then p = |A|/(|A|+100); if A>0, p = 100/(A+100). Ensure correct handling of rounding.  
- **Vig Removal:** Given two implied probabilities p1,p2 from one book (which sum >100%), compute fair probabilities p'1 = p1/(p1+p2) and p'2 = p2/(p1+p2). Convert these back to fair odds.  
- **Edge & EV:** Calculate edge% as `(P_true - P_market) / P_market * 100`. Compute Expected Value using the standard formula: EV = (P_true × payout) - (1 - P_true) × stake. (For a $1 USDC stake, payout = odds-1).  
- **Consistency Checks:** Ensure for each two-outcome bet that after removing vig, p'1 + p'2 = 1. All outputs (edges, EV) should be post-fee (if fee was subtracted from original probabilities). Include unit tests for all conversion functions.  

## Backend Implementation (FastAPI)
- **Modular Services:** Structure the backend with separate service classes or modules for each data source (PolymarketService, OddsService, DataGolfService) and one for calculations. Each service encapsulates the API calls and parsing logic.  
- **Endpoints:** Define REST endpoints such as:  
  - GET /api/opportunities – returns a list of bet opportunities.  
  - GET /api/odds/{sport} – returns raw/normalized odds data for a sport.  
  - GET /api/golf – returns current DG +EV golf bets.  
- **Data Storage:** Use SQLite initially. Create tables for OddsLog, APICallLog, MarketSnapshot. Migrate to Postgres later.  
- **Caching:** Implement caching to avoid overpulling (e.g. fastapi-cache).  
- **HTTP Client:** Use httpx (async) or requests with timeouts and retries. Respect rate limits.  
- **Error Handling:** Gracefully handle API failures. Log errors. Return HTTP 503 if upstream data is unavailable.  
- **Deployment:** Containerize with Docker. Use uvicorn/gunicorn, Nginx. Configure health checks.  

## Frontend Implementation (SwiftUI)
- **Overall UI:** Create a TabView with three tabs: All Sports, Golf (DG), and Settings.  
- **Data Fetching:** Use URLSession or async/await to call backend endpoints and decode JSON via Codable.  
- **All Sports Tab:** Display a List of opportunities sorted by EV%. Each row shows: teams/players, sport, source odds (Polymarket vs sportsbook), and EV%. Allow filtering via Pickers/Sliders.  
- **Golf Tab:** Similar list but only golf bets (from DataGolf). Show golfer, event, DG win-prob, sportsbook odds, EV%.  
- **Bet Detail View:** Show all information: odds (Polymarket, each book’s line), computed fair odds, edge%, EV. Indicate data freshness.  
- **Settings Tab:** Include controls for preferences: Fee Cushion slider, refresh interval, default EV threshold. Toggle for Developer Mode (shows all raw opportunities).  

## Fee & Tax Adjustments
- **Fees:** Apply a 2.5% fee on Polymarket or exchange bets. Deduct from implied payouts. Make adjustable in Settings.  
- **Taxes:** Optionally allow user to set a tax rate to adjust EV. Default is pre-tax.  
- **Docs:** Note that Polymarket claims no fees, but we assume 2.5% as a cushion.  

## Logging & Monitoring
- **Logging:** Use Python logging for key actions. Log API fetches, odds updates, errors.  
- **Metrics:** Track API calls, success/error rates.  
- **Odds History:** Store snapshots of odds over time in DB.  
- **Alerts:** Optional Slack/Discord alerts on repeated failures.  

## Backlog & Roadmap
1. Multi-outcome market support.  
2. Odds movement tracking.  
3. AI/ML per-market predictive models.  
4. Live betting feeds (later due to cost).  
5. User features: accounts, notifications, parlays, Kelly criterion, etc.  

## API References & Libraries
- **Polymarket API:** Gamma API (markets, events, sports tags).  
- **The Odds API:** v4 sports odds API.  
- **DataGolf API:** `preds/pre-tournament` endpoint.  
- **Python:** requests/httpx, pydantic, uvicorn, SQLAlchemy, pytest.  
- **Swift:** URLSession, Codable, SwiftUI, Combine.  
