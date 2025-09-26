# Issue 092625-6: Define Core Tables (APICallLog, OddsLog, MarketSnapshot)

**Priority**: High  
**Component**: Backend / Database  
**Beta Blocker**: Yes (required for data persistence)  
**Discovered**: 2025-09-26  
**Status**: RESOLVED  
**Resolved**: 2025-09-26

## Problem Description

We need core database tables to store API call metadata, normalized odds, and periodic market snapshots to support analysis, logging, and frontend views.

## Investigation Areas

1. Table schemas aligned with `plan.md` requirements.  
2. Indexes and retention strategy for logs/snapshots.  
3. Migration naming and seed strategy.  

## Expected Behavior

Tables exist with proper columns, constraints, and indexes. Migrations create them and can be applied on clean environments without manual steps.

## Files to Investigate

- `backend/app/db/models/*.py` (to be added)  
- `backend/alembic/versions/*`  

## Root Cause Analysis

1. **Primary Cause**: No persistence structures defined yet.  
2. **Contributing Factors**: Multiple services write distinct data forms.  
3. **Why It Happened**: Early setup phase.  

## Solution Implemented

### 1. Models and Migrations (✅ Complete)
- Define `APICallLog`, `OddsLog`, `MarketSnapshot` SQLAlchemy models.  
- Generate Alembic migration with tables and indexes.  

### Code Changes

**File Modified**: `N/A - new models and migrations were added`

**Before**:
```text
No tables for logs/snapshots.
```

**After**:
```text
backend/app/db/models/api_call_log.py
backend/app/db/models/odds_log.py
backend/app/db/models/market_snapshot.py
backend/alembic/versions/0002_core_tables.py
```

## Testing Requirements

### Manual Testing Steps
1. Run Alembic upgrade head.  
2. Insert sample rows and query back via a shell/script.  

### Test Scenarios
- [x] Migrations apply without error  
- [x] Indexes present on queried columns  

## Status

**Current Status**: RESOLVED  
**Last Updated**: 2025-09-26

### Implementation Checklist
- [x] Define models  
- [x] Create migration  
- [x] Add indexes  

### Completion Criteria (Ready for User Testing)
- [x] Tables created via migration  
- [x] CRUD works in a smoke script  
- [x] Ready for user testing  
- [x] Any blockers clearly documented  

### User Testing Confirmation
- [x] User ran migration and confirms tables exist  
- [x] User approves moving to done/complete  

## Result

Core tables exist with migrations and indexes, enabling reliable storage and query of logs and snapshots.

---

## User Confirmation & Actions Required

- Confirm any additional fields needed (e.g., request payload size, error codes).  
- Confirm retention strategy (how long to keep logs/snapshots).  

## Definition of Done (including user confirmations)

- Migrations create and verify tables.  
- User confirms schema fields and retention approach.
