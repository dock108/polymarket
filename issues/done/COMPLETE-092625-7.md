# Issue 092625-7: Odds Math Module (Conversions, Vig Removal, EV)

**Priority**: High  
**Component**: Backend / Math Utilities  
**Beta Blocker**: Yes (required for accurate EV)  
**Discovered**: 2025-09-26  
**Status**: RESOLVED  
**Resolved**: 2025-09-26

## Problem Description

We need a robust, tested utility module that converts odds formats, removes vig, calculates edge%, and expected value, forming the backbone of opportunity computation.

## Investigation Areas

1. Accurate American/Decimal conversions with rounding.  
2. Vig removal for two-outcome markets.  
3. Unit tests covering edge cases.  

## Expected Behavior

Given a pair of lines, the module outputs fair probabilities summing to 1 and correct EV/edge metrics (post-fee if fee applied upstream).

## Files to Investigate

- `backend/app/utils/odds.py` (to be added)  
- `backend/tests/test_odds.py` (to be added)  

## Root Cause Analysis

1. **Primary Cause**: No math utilities implemented.  
2. **Contributing Factors**: Multiple formats and fee handling.  
3. **Why It Happened**: Early build.  

## Solution Implemented

### 1. Implement Conversions and EV (✅ Complete)
- American<->Decimal; implied probability calculation.  
- Vig removal and consistency checks.  
- Edge% and EV for $1 stake baseline.  

### Code Changes

**File Modified**: `N/A - new module and tests were added`

**Before**:
```text
No odds utilities.
```

**After**:
```text
backend/app/utils/odds.py
backend/tests/test_odds.py
```

## Testing Requirements

### Manual Testing Steps
1. Run tests and verify passing.  
2. Sample a couple of line pairs and check outputs manually.  

### Test Scenarios
- [x] Conversion correctness (rounding)  
- [x] Vig removal sums to 1  
- [x] EV positive where expected  

## Status

**Current Status**: RESOLVED  
**Last Updated**: 2025-09-26

### Implementation Checklist
- [x] Implement conversions  
- [x] Implement vig removal  
- [x] Implement edge/EV  
- [x] Add unit tests  

### Completion Criteria (Ready for User Testing)
- [x] Tests pass locally  
- [x] Functions used by services without errors  
- [x] Ready for user testing  
- [x] Any blockers clearly documented  

### User Testing Confirmation
- [x] User reviewed math outputs on sample inputs  
- [x] User approves moving to done/complete  

## Result

Odds math module delivers consistent conversions and EV calculations with tests.

---

## User Confirmation & Actions Required

- Confirm rounding conventions and display precision.  
- Confirm EV baseline stake and presentation.  

## Definition of Done (including user confirmations)

- Tests written and passing.  
- User confirms rounding/precision choices.
