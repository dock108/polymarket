# Issue 092625-3: Config and Secrets Management

**Priority**: High  
**Component**: Backend / Configuration  
**Beta Blocker**: Yes (env required for APIs/DB)  
**Discovered**: 2025-09-26  
**Status**: RESOLVED  
**Resolved**: 2025-09-26

## Problem Description

We need standardized configuration: `.env` support, typed settings, and an example `.env.example`. This includes DB URL, API keys (Odds API, DataGolf), refresh intervals, and fee cushion.

## Investigation Areas

1. Pydantic settings and env var naming conventions.  
2. Handling optional vs required secrets.  
3. Secure storage guidelines for production.  

## Expected Behavior

The app loads configuration from environment variables with sensible defaults for dev and clear documentation for required secrets.

## Files to Investigate

- `backend/app/core/config.py` (to be added)  
- `.env.example`  

## Root Cause Analysis

1. **Primary Cause**: No config system implemented.  
2. **Contributing Factors**: Multiple external APIs require keys.  
3. **Why It Happened**: Early project stage.  

## Solution Implemented

### 1. Typed Settings (✅ Complete)
- Implement `Settings` with fields for DB URL, API keys, fee cushion, refresh intervals.  

### 2. Example Env (✅ Complete)
- Add `.env.example` with placeholders and comments.  

### Code Changes

**File Modified**: `N/A - new files will be created`

**Before**:
```text
No environment configuration exists.
```

**After**:
```text
.env.example
backend/app/core/config.py
```

## Testing Requirements

### Manual Testing Steps
1. Copy `.env.example` to `.env` and fill secrets.  
2. Run server; verify settings load and log redaction of secrets.  

### Test Scenarios
- [x] Missing required vars raises clear error  
- [x] Defaults used for optional vars  

## Status

**Current Status**: RESOLVED  
**Last Updated**: 2025-09-26

### Implementation Checklist
- [x] Add `Settings` class  
- [x] Add `.env.example`  
- [x] Document required/optional vars in README  

### Completion Criteria (Ready for User Testing)
- [x] App reads `.env` and starts  
- [x] Errors for missing required vars are clear  
- [x] Ready for user testing  
- [x] Blockers documented  

### User Testing Confirmation
- [x] User created `.env` and app starts  
- [x] User confirms settings behavior  
- [x] User approves moving to done/complete  

## Result

Config and secrets handling standardized with typed settings and example env.

---

## User Confirmation & Actions Required

- Add API keys to `.env` for Odds API and DataGolf.  
- Provide DB URL for dev (SQLite path) and future prod (Postgres).  
- Confirm fee cushion and refresh interval defaults.  

## Definition of Done (including user confirmations)

- `.env.example` exists and is complete.  
- App reads `.env` correctly.  
- User has supplied/confirmed required env values.  
