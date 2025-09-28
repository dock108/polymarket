# API Documentation

Base URL: `http://localhost:8000`

## Health
GET `/health`
- 200 `{ "status": "ok" }`

## Opportunities
GET `/api/opportunities`
- Returns an array of Opportunity objects
- Fields:
  - `id`, `source`, `title`, `sport?`, `event_id?`, `market_id?`
  - `canonical_event_key?`, `yes_probability?`, `price?`
  - `ev_usd_per_share?`, `ev_percent?`
  - `comparison_basis?` (e.g., `none`, `sportsbook_fair`), `comparison_sources?` (e.g., `["odds_api"]`)
  - `updated_at?`, `is_stale?`
  - Provenance: `source_attribution?`, `inputs?`, `calc_notes?`

Policy:
- When only Polymarket is available, EV baseline is 0 and `comparison_basis = "none"`.
- When sportsbook fair probabilities are available, `comparison_basis = "sportsbook_fair"` and EV is computed against PM price.

Example:
```json
[
  {
    "id": "polymarket:12345",
    "source": "polymarket",
    "title": "Team A vs Team B",
    "sport": "basketball_nba",
    "canonical_event_key": "basketball_nba:team_a_vs_team_b",
    "price": 0.45,
    "yes_probability": 0.47,
    "ev_percent": 4.4,
    "comparison_basis": "sportsbook_fair",
    "comparison_sources": ["odds_api"],
    "updated_at": "2025-09-26T00:00:00Z",
    "is_stale": false
  }
]
```

### Freshness Meta
GET `/api/opportunities/meta`
- Returns metadata wrapper and items with `is_stale`
- Fields: `as_of`, `staleness_seconds`, `items[]`

## Odds by Sport
GET `/api/odds/{sport}`
- Returns an array of events with bookmaker lines
- `EventLines`: `sport`, `event_id`, `title`, `canonical_event_key?`, `selected_bookmaker?`, `lines[]`
- `BookLine`: `bookmaker`, `market`, `side`, `american_odds?`, `decimal_odds?`, `point?`, `fair_probability?`, `fair_decimal_odds?`

Example:
```json
[
  {
    "sport": "basketball_nba",
    "event_id": "evt1",
    "title": "Rockets vs Thunder",
    "canonical_event_key": "basketball_nba:rockets_vs_thunder",
    "selected_bookmaker": "pinnacle|betfair",
    "lines": [
      {"bookmaker":"pinnacle","market":"h2h","side":"Thunder","american_odds":-150,"decimal_odds":1.67,"fair_probability":0.58,"fair_decimal_odds":1.72}
    ]
  }
]
```

## Debug
GET `/api/debug/opportunity/{id}`
- Returns detailed trace for a specific opportunity (for troubleshooting)
- Includes the opportunity fields and compact provenance

## Golf (placeholder)
GET `/api/golf`
- Currently returns `[]` (backlogged features)
