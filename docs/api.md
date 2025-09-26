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
  - `yes_probability?`, `price?`, `ev_usd_per_share?`, `ev_percent?`, `updated_at?`

Example:
```json
[
  {
    "id": "polymarket:12345",
    "source": "polymarket",
    "title": "Team A vs Team B",
    "sport": "nba",
    "price": 0.45,
    "yes_probability": 0.47,
    "ev_percent": 0.044,
    "updated_at": "2025-09-26T00:00:00Z"
  }
]
```

## Odds by Sport
GET `/api/odds/{sport}`
- Returns an array of events with bookmaker lines
- `EventLines`: `sport`, `event_id`, `title`, `lines[]`
- `BookLine`: `bookmaker`, `market`, `side`, `american_odds?`, `decimal_odds?`, `point?`, `fair_probability?`, `fair_decimal_odds?`

Example:
```json
[
  {
    "sport": "nba",
    "event_id": "evt1",
    "title": "Rockets @ Thunder",
    "lines": [
      {"bookmaker":"pinnacle","market":"h2h","side":"Thunder","american_odds":-150,"decimal_odds":1.67,"fair_probability":0.58,"fair_decimal_odds":1.72}
    ]
  }
]
```

## Golf (placeholder)
GET `/api/golf`
- Currently returns `[]` (backlogged features)
