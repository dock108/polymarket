# Polymarket + Sportsbook Edge Detection Architecture

This system continuously ingests live and historical data from **Polymarket** and **TheOddsAPI**, stores hourly snapshots, converts Polymarket data into sportsbook-compatible structures, and eventually trains an ML model to confirm whether Polymarket offers a superior price after accounting for fees and slippage.

---

## 🧩 Overview

**Goal:**  
Identify and verify consistent pricing edges where Polymarket markets outperform traditional sportsbooks — first via direct comparison, later via a trained model built from months of historical data.

**Core Components:**
1. **Data Ingestion:** Polymarket markets & order books + TheOddsAPI live & historical odds.  
2. **Storage:** Operational DB (Postgres/Timescale) and Data Lake (S3/GCS).  
3. **ETL & Normalization:** Map Polymarket markets to sportsbook format.  
4. **Feature Engineering:** Build time-based, line-movement, and pricing-delta features.  
5. **Modeling:** Train ML models on 2–3 months of historical data to confirm market edges.  
6. **Comparator & Alerts:** Compare Polymarket vs sportsbook in real time and flag edges.  
7. **Monitoring:** Observability, task health, and data freshness alerts.

---

## 🧱 System Architecture (Mermaid Diagram)

```mermaid
flowchart LR
  %% ============ SOURCES ============
  subgraph SRC[Data Sources]
    PM[Polymarket<br/>Markets & Order Books]
    OA[TheOddsAPI<br/>Sportsbook Lines (live)]
    OAH[TheOddsAPI<br/>Historical Lines]
  end

  %% ============ ORCHESTRATION ============
  subgraph ORCH[Orchestration & Workers]
    AF[Scheduler / Orchestrator<br/>(Airflow/Celery/Apscheduler)]
    W1[Ingest Worker: Polymarket]
    W2[Ingest Worker: OddsAPI Live]
    W3[Ingest Worker: OddsAPI Historical]
    W4[ETL & Schema Mapper<br/>(PM→Sportsbook layout)]
    W5[Feature Builder]
    W6[Model Trainer]
    W7[Comparator & Signals]
  end

  %% ============ STORAGE ============
  subgraph STG[Storage]
    subgraph OLTP[Operational DB (Postgres/Timescale)]
      DBM[markets]
      DBOB[order_books_hourly_snapshots]
      DBOAL[oddsapi_live]
      DBOAH[oddsapi_historical_hourly]
      MAP[market_mappings & team_aliases]
      FEAT[features_latest]
      SIG[signals]
      EXEC[executions & fills]
      COST[cost_models & fee_tables]
    end
    subgraph DL[Data Lake (S3/GCS)]
      RAW[raw/parquet/<br/>pm, oddsapi, snapshots]
      TRAIN[ml/training_sets]
      MODELS[ml/models & metrics]
    end
    FS[Feature Store (DuckDB/Feast/Parquet)]
  end

  %% ============ SERVING / OUTPUT ============
  subgraph SVC[Serving & Ops]
    API[Model & Comparator API]
    UI[Ops UI / Dashboards<br/>(Streamlit/Next.js/Grafana)]
    ALERT[Alerting (Slack/Email/Webhooks)]
    BOT[Trader Bot (optional)]
    MON[Monitoring & Logs<br/>(Prom/Grafana/ELK)]
  end

  %% --- Edges: Ingestion ---
  PM -->|markets poll| W1
  PM -->|order book 1h snapshot| W1
  OA -->|live odds poll| W2
  OAH -->|backfill/hourly| W3

  %% --- Workers to storage ---
  W1 --> RAW
  W1 --> DBM
  W1 --> DBOB

  W2 --> RAW
  W2 --> DBOAL

  W3 --> RAW
  W3 --> DBOAH

  %% --- ETL / Mapping to sportsbook layout ---
  W4 --> MAP
  DBM --> W4
  DBOB --> W4
  MAP --> W4
  W4 --> FS
  W4 --> FEAT

  %% --- Feature building & model training ---
  FEAT --> W5
  DBOAH --> W5
  DBOAL --> W5
  W5 --> FS
  W5 --> TRAIN

  TRAIN --> W6
  COST --> W6
  W6 --> MODELS
  W6 --> API

  %% --- Live comparison & signals ---
  API --> W7
  FS --> W7
  DBOAL --> W7
  DBM --> W7
  COST --> W7
  W7 --> SIG
  W7 --> ALERT
  W7 --> UI

  %% --- Execution (optional) ---
  SIG --> BOT
  BOT --> EXEC
  EXEC --> UI

  %% --- Monitoring ---
  ORCH --> MON
  STG --> MON
  SVC --> MON


⸻

🔁 Dataflow / Handshakes (Sequence)

sequenceDiagram
  autonumber
  participant Sch as Scheduler
  participant PM as Polymarket API
  participant OA as OddsAPI (Live)
  participant OAH as OddsAPI (Hist)
  participant WPM as Worker: PM Ingest
  participant WOAL as Worker: Odds Live
  participant WOAH as Worker: Odds Hist
  participant ETL as ETL: PM→Sportsbook Layout
  participant DB as OLTP DB
  participant DL as Data Lake
  participant FS as Feature Store
  participant MT as Model Trainer
  participant API as Model/Comparator API
  participant CMP as Comparator
  participant AL as Alerts/Signals
  participant COST as Fees/Slippage Model

  Sch->>WPM: Every 60s (markets); Every 1h (order book snapshot)
  WPM->>PM: GET /markets & orderbooks
  PM-->>WPM: JSON markets + aggregated book
  WPM->>DL: write raw/parquet/pm/...
  WPM->>DB: upsert markets; insert order_books_hourly_snapshots

  Sch->>WOAL: Every 60–120s
  WOAL->>OA: GET /odds (live)
  OA-->>WOAL: JSON odds by book/sport/event
  WOAL->>DL: write raw/parquet/oddsapi/live
  WOAL->>DB: upsert oddsapi_live

  Sch->>WOAH: Hourly (and backfill windows)
  WOAH->>OAH: GET /odds (historical)
  OAH-->>WOAH: JSON historical
  WOAH->>DL: write raw/parquet/oddsapi/hist
  WOAH->>DB: insert oddsapi_historical_hourly

  Sch->>ETL: On PM/Odds arrivals (event-driven or 5-min batch)
  ETL->>DB: read markets, order_books_hourly, odds, mappings
  ETL->>DB: write normalized features_latest (+ entity mapping)
  ETL->>FS: push standardized features

  Sch->>MT: Nightly (or after 60–90 days of data)
  MT->>DB: read features + cost_models
  MT->>DL: write training_sets; store models & metrics
  MT->>API: register model (versioned)

  loop Live loop (1–2 min)
    CMP->>DB: fetch latest features + odds + PM markets
    CMP->>API: score edge; expected value
    CMP->>COST: apply fees, vig, slippage, fill prob
    CMP-->>AL: emit signal if EV > threshold + liquidity OK
  end


⸻

⏱ Scheduling & Cadence (Gantt)

gantt
  dateFormat  HH:mm
  title Ingestion & Pipeline Cadence (example window)
  section Polymarket
  Markets poll (30–60s)        :done, pm1, 00:00, 00:05
  Order book snapshot (1h)      :active, pm2, 00:00, 01:00
  section OddsAPI
  Live odds poll (60–120s)      :active, oa1, 00:00, 00:10
  Historical backfill (hourly)  :active, oa2, 00:05, 00:30
  section ETL/Mapping
  Normalize + map entities (5m) :etl1, 00:02, 00:07
  Feature build (rolling)       :etl2, 00:07, 00:12
  section Modeling
  Nightly train/eval            :mt1, 23:00, 01:00
  section Compare & Signals
  Edge calc (rolling 1–2m)      :cmp1, 00:00, 00:10


⸻

🧠 Key Implementation Notes

Entity Mapping
	•	Normalize team names, league IDs, and event references into a market_mappings table.
	•	Use an alias resolver so Polymarket and sportsbook data align 1-to-1.

Cost Model
	•	Table for:
	•	Per-venue/book fees and vig.
	•	Expected slippage based on order depth and size.
	•	Fill probability (from historical fills).
	•	Liquidity cutoff rules.

Snapshots
	•	Polymarket: hourly order_books_hourly_snapshots storing best bid/ask depth and liquidity.
	•	OddsAPI: hourly historical odds mirror to align with Polymarket snapshots for trend analysis.

Features
	•	Line deltas, PM vs consensus implied probabilities, drift rates, liquidity decay, etc.
	•	Rolling 1 h/6 h/24 h statistics for volatility and mean-reversion markers.

Model Training
	•	Train after 2–3 months of data:
	•	Logistic classifier for “edge validity.”
	•	Regression model for EV magnitude.
	•	Store in /ml/models with MLflow tracking.
	•	Double confirm that model + Polymarket edge > sportsbook after costs.

Comparator Logic
	•	Signal triggers only when:
	1.	Model confidence ≥ threshold.
	2.	Polymarket shows superior price vs sportsbook.
	3.	After applying fees/slippage, EV > min target (e.g. +3%).
	4.	Liquidity ≥ minimum trade size.

Monitoring
	•	Grafana/Prometheus: latency, job success, freshness, data completeness.
	•	Slack Alerts: edge detections, missing leagues, or alias mismatches.
	•	ELK/Cloud Logging: full raw traces for ingestion and API responses.

⸻

🧩 Example Tech Stack

Layer	Preferred Tools
Ingestion	Python workers (Requests + Pydantic), Celery/Airflow
Storage	PostgreSQL + TimescaleDB, S3 (parquet)
Processing	Pandas / Polars ETL, DuckDB Feature Store
Modeling	scikit-learn / XGBoost / LightGBM
API / Serving	FastAPI or Flask
Dashboard	Streamlit / Next.js + Grafana
Monitoring	Prometheus + Grafana + ELK
Alerts	Slack / Email / Webhooks


⸻

🧩 Next Steps
	1.	Define schema migrations (markets, order_books_hourly_snapshots, oddsapi_live, etc.).
	2.	Build ingestion scripts with idempotent inserts and retry logic.
	3.	Implement entity mapping + ETL normalization layer.
	4.	Add feature generation jobs and store in feature store.
	5.	After 2–3 months of data, begin model training and evaluation.
	6.	Deploy Comparator API + alerting pipeline.
	7.	Add trader bot for simulated or real execution.

⸻
