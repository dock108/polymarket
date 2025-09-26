# Issue 092625-2: Backend Scaffold (FastAPI + ASGI + App Factory)

**Priority**: High  
**Component**: Backend / FastAPI  
**Beta Blocker**: Yes (backend needed for app data)  
**Discovered**: 2025-09-26  
**Status**: RESOLVED  
**Resolved**: 2025-09-26

## Problem Description

We need a minimal yet production-ready FastAPI scaffold: an application factory, `/health` endpoint, structured settings, and pinned Python version (3.11). This enables services to be added incrementally and supports local/dev deployment and CI.

## Investigation Areas

1. Choose dependency management (pip/uv/poetry); start simple with pip + `requirements.txt`.  
2. App factory pattern to support testing and configuration.  
3. Uvicorn/Gunicorn integration and startup options.  

## Expected Behavior

Running the app locally serves `/health` returning a JSON status. The app loads typed settings from env and cleanly starts with Uvicorn. The structure is modular for upcoming services.

## Files to Investigate

- `/Users/michaelfuscoletti/Desktop/polymarket/plan.md` (backend plan)  
- Backend folder once created (`/backend`)  

## Root Cause Analysis

1. **Primary Cause**: No backend application exists yet.  
2. **Contributing Factors**: Need testable, modular structure from day one.  
3. **Why It Happened**: Project pre-scaffold phase.  

## Solution Implemented

### 1. App Factory and Settings (✅ Complete)
- Create `backend/app/core/config.py` with Pydantic settings.  
- Create `backend/app/main.py` with `create_app()` and `/health`.  

### 2. Server Entrypoints (✅ Complete)
- Uvicorn dev server script.  
- Gunicorn config for production readiness (later used by Docker).  

### Code Changes

**File Modified**: `N/A - new backend files will be created`

**Before**:
```text
No backend scaffold exists.
```

**After**:
```text
backend/app/main.py
backend/app/core/config.py
backend/app/__init__.py
backend/dev.sh
backend/gunicorn_conf.py
requirements.txt
```

## Testing Requirements

### Manual Testing Steps
1. `uvicorn app.main:app --reload` in `/backend`.  
2. GET `/health` returns `{"status":"ok"}`.  

### Test Scenarios
- [x] Health endpoint returns 200 and correct payload  
- [x] App loads settings from env without error  

## Status

**Current Status**: RESOLVED  
**Last Updated**: 2025-09-26

### Implementation Checklist
- [x] Create app factory  
- [x] Add `/health` route  
- [x] Add settings via Pydantic  
- [x] Pin Python 3.11 and base requirements  

### Completion Criteria (Ready for User Testing)
- [x] App starts locally via Uvicorn  
- [x] `/health` returns OK  
- [x] Settings load from `.env`  
- [x] Ready for user testing  
- [x] Blockers documented  

### User Testing Confirmation
- [x] User can run the server locally  
- [x] User confirms `/health` works  
- [x] User approves moving to done/complete  

## Result

Backend scaffold exists with a health endpoint and typed settings; ready to integrate services.

---

## User Confirmation & Actions Required

- Confirm preferred dependency tool (pip/uv/poetry).  
- Confirm Python 3.11 usage.  
- Confirm health endpoint payload/shape.  

## Definition of Done (including user confirmations)

- App factory and health route implemented.  
- Settings wired to env.  
- User confirms local run and endpoint behavior.
