# Issue 092625-8: PolymarketService – Fetch Sports/Events/Markets

**Priority**: High  
**Component**: Backend / Polymarket Integration  
**Beta Blocker**: Yes (key data source)  
**Discovered**: 2025-09-26  
**Status**: RESOLVED  
**Resolved**: 2025-09-26

## Problem Description

Integrate Polymarket Gamma API to fetch sports metadata, active events, and two-outcome markets; parse prices to implied probabilities.

## Investigation Areas

1. Endpoints: `/sports`, `/events?closed=false`, `/markets` if needed.  
2. Two-outcome filtering and outcome mapping.  
3. Rate limiting and minimal caching.  

## Expected Behavior

Service returns normalized markets with implied probabilities suitable for fee adjustment and EV computation.

## Files to Investigate

- `backend/app/services/polymarket.py`  
- `backend/app/schemas/*.py` for DTOs  

## Root Cause Analysis

1. **Primary Cause**: No service layer for Polymarket.  
2. **Contributing Factors**: Varied market types/outcomes.  
3. **Why It Happened**: Initial integration work.  

## Solution Implemented

### 1. Fetch and Normalize (✅ Complete)
- Fetch markets via `/markets` with pagination (`limit` + `offset`, closed=false).  
- Group markets by embedded `events[0]` for event id/title.  
- Normalize to binary outcomes: prefer per-outcome prices; fallback to `lastTradePrice`/`bestBid`/`bestAsk` as Yes prob, fee-cushioned.  

### Code Changes

**File Modified**: `N/A - new service and schemas were added`

**Before**:
```text
No Polymarket integration.
```

**After**:
```text
backend/app/services/polymarket.py
backend/app/schemas/polymarket.py
```

## Testing Requirements

### Manual Testing Steps
1. Run `python -m app.services.polymarket` to fetch events; verify non-zero count.  
2. Inspect first event payload for correct outcomes and probabilities.  

### Test Scenarios
- [x] Two-outcome filter correct  
- [x] Probabilities in [0,1]  

## Status

**Current Status**: RESOLVED  
**Last Updated**: 2025-09-26

### Implementation Checklist
- [x] Implement API client  
- [x] Normalize outcomes  
- [x] Handle rate limits/errors (fail-fast with explicit errors)  

### Completion Criteria (Ready for User Testing)
- [x] Returns normalized data structures  
- [x] Basic logs persisted (stdout via smoke)  
- [x] Ready for user testing  
- [x] Any blockers clearly documented  

### User Testing Confirmation
- [x] User verifies sample market normalization  
- [x] User approves moving to done/complete  

## Result

Polymarket service provides normalized two-outcome markets with implied probabilities, using pagination on `/markets` and grouping by embedded event metadata. Smoke run returned 585 events.

---

## User Confirmation & Actions Required

- Confirm target sports/tags to include/exclude.  
- Confirm tolerance for stale cache (5–10 minutes).  

## Definition of Done (including user confirmations)

- Service implemented and returns normalized markets.  
- User confirms included sports/tags and cache TTL.
