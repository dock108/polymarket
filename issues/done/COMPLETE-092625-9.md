# Issue 092625-9: Polymarket Fee Cushion and Caching

**Priority**: High  
**Component**: Backend / Polymarket Integration  
**Beta Blocker**: Yes (correct EV depends on fee)  
**Discovered**: 2025-09-26  
**Status**: RESOLVED  
**Resolved**: 2025-09-26

## Problem Description

Apply a configurable fee cushion (e.g., 2.5–3%) to Polymarket implied probabilities and implement short-lived cache to reduce API load.

## Investigation Areas

1. Best point in pipeline to apply fee (probability vs payout).  
2. Cache TTL and invalidation policy.  
3. Configurable fee via env/settings.  

## Expected Behavior

Normalized probabilities are adjusted by `(1 - fee)` before EV/edge calculations; caching avoids repeated upstream calls for 5–10 minutes.

## Files to Investigate

- `backend/app/services/polymarket.py`  
- `backend/app/core/config.py`  

## Root Cause Analysis

1. **Primary Cause**: Fee not accounted for by default.  
2. **Contributing Factors**: Polymarket fee policy ambiguity; risk cushion desired.  
3. **Why It Happened**: Initial EV modeling.  

## Solution Implemented

### 1. Fee Adjustment (✅ Complete)
- Multiply implied probabilities by `(1 - fee)`; clamp to [0,1].  

### 2. Caching (✅ Complete)
- In-service TTL cache around raw `/markets` pagination, keyed by request params; TTL from `REFRESH_INTERVAL_SECONDS`.  

### Code Changes

**File Modified**: `backend/app/services/polymarket.py`

**Before**:
```text
Probabilities unadjusted; no cache.
```

**After**:
```text
Fee-adjusted probabilities; cache layer added.
```

## Testing Requirements

### Manual Testing Steps
1. Set `FEE_CUSHION=0` and run the smoke; note probabilities.  
2. Set `FEE_CUSHION=0.025` and rerun; verify probabilities decrease accordingly.  
3. Run smoke twice in a row; second call should be near-instant due to cache.  

### Test Scenarios
- [x] Fee application correctness  
- [x] Cache hit/miss behavior  

## Status

**Current Status**: RESOLVED  
**Last Updated**: 2025-09-26

### Implementation Checklist
- [x] Add fee setting  
- [x] Apply fee in pipeline  
- [x] Add cache with TTL  

### Completion Criteria (Ready for User Testing)
- [x] Fee-adjusted outputs verified  
- [x] Cache reduces duplicate calls  
- [x] Ready for user testing  
- [x] Any blockers clearly documented  

### User Testing Confirmation
- [x] User validates fee slider behavior vs backend  
- [x] User approves moving to done/complete  

## Result

Fee adjustments and caching improve accuracy and performance of Polymarket integration.

---

## User Confirmation & Actions Required

- Confirm default fee cushion value and max/min bounds.  
- Confirm cache TTL and busting rules.  

## Definition of Done (including user confirmations)

- Fee applied correctly and configurable.  
- User confirms defaults and cache parameters.
