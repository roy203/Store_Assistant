# Task: retrieve_store LangChain Tool

## Description
Implement the `retrieve_store` LangChain `@tool`-decorated function in `store_assistant/agent/tools.py`. This tool verifies the passphrase, performs a case-insensitive store lookup, and returns the phone number or an appropriate error string.

## Background
The passphrase check is a single-attempt operation at the tool level. Retry logic (up to 3 attempts) is managed by the agent in Step 6 — the tool simply returns success or a "wrong passphrase" string on each call. The passphrase is loaded from `config.store_lookup_passphrase` (from `.env`).

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See FR-06 through FR-10, and the "agent/tools.py" section.

## Technical Requirements
1. Decorate with `@tool` from `langchain_core.tools`
2. Function signature: `retrieve_store(name: str, passphrase: str) -> str`
3. Docstring must clearly describe when to use this tool
4. Compare `passphrase` against `config.store_lookup_passphrase` using case-sensitive equality
5. If passphrase is wrong, return a specific sentinel string: `"WRONG_PASSPHRASE"` — the agent uses this to count retry attempts
6. If passphrase is correct, call `db.get_store(name)`
7. If store not found, return `"STORE_NOT_FOUND"`
8. If store found, return the phone number string
9. Write tests in `store_assistant/tests/test_passphrase.py`

## Dependencies
- Step 2 (`db/database.py` CRUD) must be complete
- Step 1 (`config.py`) must be complete so passphrase is loadable

## Implementation Approach
1. Import `tool`, `config`, and `get_store` from their respective modules
2. Passphrase check: `if passphrase != config.store_lookup_passphrase: return "WRONG_PASSPHRASE"`
3. DB lookup: `result = get_store(name)`
4. Return `"STORE_NOT_FOUND"` if `result is None`, else `result["phone"]`
5. Use `monkeypatch` in tests to inject passphrase and temp DB

## Acceptance Criteria

1. **Correct Passphrase Returns Phone**
   - Given a store "Walmart" with phone "5551234567" in the DB and correct passphrase provided
   - When `retrieve_store("walmart", correct_passphrase)` is called
   - Then `"5551234567"` is returned

2. **Wrong Passphrase Returns Sentinel**
   - Given any store name and an incorrect passphrase
   - When `retrieve_store("Walmart", "wrongpass")` is called
   - Then `"WRONG_PASSPHRASE"` is returned and DB is NOT queried

3. **Store Not Found Returns Sentinel**
   - Given correct passphrase but "Target" does not exist in DB
   - When `retrieve_store("Target", correct_passphrase)` is called
   - Then `"STORE_NOT_FOUND"` is returned

4. **Lookup Is Case-Insensitive**
   - Given "Walmart" saved with uppercase name
   - When `retrieve_store("walmart", correct_passphrase)` is called
   - Then the correct phone is returned

5. **Tool Is Decorated and Has Docstring**
   - Given the `retrieve_store` function
   - When checking its type and `.description`
   - Then it is a LangChain `StructuredTool` with a non-empty description

## Metadata
- **Complexity**: Low
- **Labels**: langchain, tools, agent, retrieve, passphrase, security
- **Required Skills**: LangChain tools API, Python, pytest monkeypatch
