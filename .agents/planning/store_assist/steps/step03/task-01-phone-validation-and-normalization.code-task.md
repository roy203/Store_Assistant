# Task: Phone Validation and Normalization

## Description
Implement `validate_phone(phone: str) -> bool` and `normalize_phone(phone: str) -> str` utility functions in `store_assistant/agent/utils.py`. These handle US phone number validation and normalization before any store is saved.

## Background
The spec requires US-only phone validation with reprompting on invalid input. Accepted formats include `(555) 555-5555`, `555-555-5555`, `5555555555`, `+15555555555`, and `555.555.5555`. Normalization strips formatting to produce a consistent 10-digit string for storage.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See FR-02, FR-03, and the "Step 3: Phone Validation Utility" section of the implementation plan.

## Technical Requirements
1. `validate_phone(phone: str) -> bool` — returns `True` if the phone matches a valid US format, `False` otherwise
2. `normalize_phone(phone: str) -> str` — strips all non-digit characters; if result is 11 digits starting with `1`, strips the leading `1`; returns 10-digit string
3. Accepted input formats: `(555) 555-5555`, `555-555-5555`, `5555555555`, `+15555555555`, `555.555.5555`
4. Rejected inputs: fewer than 10 digits, more than 11 digits, non-numeric characters that don't form a valid pattern, empty string
5. Use a single regex approach: strip non-digits, then check digit count
6. Place both functions in `store_assistant/agent/utils.py`
7. Write tests in `store_assistant/tests/test_phone_validation.py`

## Dependencies
- Step 1 scaffold must be complete so `store_assistant/agent/` package exists

## Implementation Approach
1. In `validate_phone`: strip all non-digit characters from input, check if result is exactly 10 digits OR 11 digits starting with `"1"`
2. In `normalize_phone`: strip non-digits; if 11 digits starting with `"1"`, strip first digit; return remaining 10 digits
3. Handle edge cases: `None` input, empty string, all-letters string
4. Write parametrized pytest tests covering all valid and invalid cases

## Acceptance Criteria

1. **Valid US Formats Accepted**
   - Given phone strings: `"(555) 555-5555"`, `"555-555-5555"`, `"5555555555"`, `"+15555555555"`, `"555.555.5555"`
   - When `validate_phone()` is called on each
   - Then all return `True`

2. **Invalid Formats Rejected**
   - Given phone strings: `"123"`, `"abcdefghij"`, `"12345678901234"`, `""`, `"555-55-555"`
   - When `validate_phone()` is called on each
   - Then all return `False`

3. **Normalization Strips Formatting**
   - Given `"(555) 555-5555"`
   - When `normalize_phone()` is called
   - Then `"5555555555"` is returned

4. **Normalization Strips Leading Country Code**
   - Given `"+15555555555"`
   - When `normalize_phone()` is called
   - Then `"5555555555"` is returned (10 digits, no leading 1)

5. **Validate and Normalize Are Consistent**
   - Given any string where `validate_phone()` returns `True`
   - When `normalize_phone()` is called
   - Then the result is always exactly 10 digits

## Metadata
- **Complexity**: Low
- **Labels**: validation, phone, regex, utility
- **Required Skills**: Python regex, pytest parametrize
