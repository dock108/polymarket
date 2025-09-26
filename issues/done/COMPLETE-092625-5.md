# Issue 092625-5: Database Setup (SQLite + SQLAlchemy + Alembic)

**Priority**: High  
**Component**: Backend / Database  
**Beta Blocker**: Yes (persistence needed)  
**Discovered**: 2025-09-26  
**Status**: RESOLVED  
**Resolved**: 2025-09-26

## Problem Description

We need an initial database setup using SQLite for development with SQLAlchemy ORM and Alembic migrations to allow a smooth later switch to Postgres.

## Investigation Areas

1. SQLAlchemy session management patterns for FastAPI.  
2. Alembic configuration and autogenerate strategy.  
3. SQLite file path and Docker volume mapping.  

## Expected Behavior

The backend can connect to SQLite via a configured URL. Alembic migrations initialize the schema and can be run via a simple command.

## Files to Investigate

- `backend/app/db/session.py`, `backend/app/db/base.py`  
- `alembic.ini`, `backend/alembic/`  

## Root Cause Analysis

1. **Primary Cause**: No DB layer defined.  
2. **Contributing Factors**: Need migration discipline from the start.  
3. **Why It Happened**: Early phase.  

## Solution Implemented

### 1. ORM and Session (✅ Complete)
- Configure engine, sessionmaker, Base.  

### 2. Alembic (✅ Complete)
- Initialize Alembic, base migration, and scripts for upgrade/downgrade.  

### Code Changes

**File Modified**: `N/A - new files were added`

**Before**:
```text
No database configuration.
```

**After**:
```text
backend/app/db/session.py
backend/app/db/base.py
backend/alembic.ini
backend/alembic/env.py
backend/alembic/versions/0001_initial.py
```

## Testing Requirements

### Manual Testing Steps
1. Run `alembic -c alembic.ini upgrade head`.  
2. Verify DB file exists and tables created.  

### Test Scenarios
- [x] Alembic upgrade works  
- [x] Session can query a simple table (smoke)  

## Status

**Current Status**: RESOLVED  
**Last Updated**: 2025-09-26

### Implementation Checklist
- [x] Add SQLAlchemy engine/session  
- [x] Initialize Alembic  
- [x] Create base migration  

### Completion Criteria (Ready for User Testing)
- [x] Schema initializes via Alembic  
- [x] App connects and queries successfully  
- [x] Ready for user testing  
- [x] Blockers documented  

### User Testing Confirmation
- [x] User ran migration locally  
- [x] User confirms DB file/tables present  
- [x] User approves moving to done/complete  

## Result

Database layer established with migrations, ready for models. DB created at `backend/data/dev.db` by default; Docker uses repo `data/` volume.

---

## User Confirmation & Actions Required

- Confirm SQLite path/location and filename preference.  
- Confirm migration naming convention and workflow.  

## Definition of Done (including user confirmations)

- Alembic migrations run cleanly.  
- User validated DB initialization locally.
