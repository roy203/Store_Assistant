# Task: Database CRUD Operations

## Description
Implement `upsert_store`, `get_store`, and `save_summary` functions in `store_assistant/db/database.py`. These are the complete data access layer consumed by the agent tools and summary persistence logic.

## Background
Three operations are needed: upsert a store (insert or update on duplicate name), case-insensitive store lookup by name, and insert a conversation summary record. All operations must be atomic and use the context manager pattern established in task-01.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See "db/database.py" Public Interface section for the exact function signatures.

## Technical Requirements
1. `upsert_store(name: str, phone: str, db_path: str = None) -> None` — INSERT OR REPLACE into `stores`; also updates `updated_at` timestamp
2. `get_store(name: str, db_path: str = None) -> dict | None` — SELECT with `WHERE LOWER(name) = LOWER(?)`, returns `{"name": ..., "phone": ...}` or `None`
3. `save_summary(session_id: str, summary_text: str, stores_saved: int, stores_retrieved: int, session_start: datetime, session_end: datetime, db_path: str = None) -> None` — INSERT into `conversation_summaries`, computing `duration_seconds` internally
4. All functions call `init_db()` as their first operation to ensure schema exists
5. Return types must be exact as specified — no exceptions for "not found", return `None`

## Dependencies
- Task 01 of this step (schema and init) must be complete

## Implementation Approach
1. `upsert_store`: use `INSERT OR REPLACE INTO stores (name, phone, updated_at) VALUES (?, ?, ?)` — SQLite's `COLLATE NOCASE` on the unique index handles case-insensitive deduplication
2. `get_store`: use `conn.row_factory = sqlite3.Row` to return dict-like results; return `dict(row)` or `None`
3. `save_summary`: compute `duration_seconds = (session_end - session_start).total_seconds()`; insert all fields
4. Write comprehensive tests in `store_assistant/tests/test_database.py` covering all cases listed in the plan

## Acceptance Criteria

1. **Upsert Inserts New Store**
   - Given an empty database
   - When `upsert_store("Walmart", "5551234567")` is called
   - Then `get_store("Walmart")` returns `{"name": "Walmart", "phone": "5551234567"}`

2. **Upsert Updates Existing Store**
   - Given a database with "Walmart" stored with phone "5551234567"
   - When `upsert_store("Walmart", "5559876543")` is called
   - Then `get_store("Walmart")` returns phone `"5559876543"` and only one record exists

3. **Case-Insensitive Lookup**
   - Given "Walmart" saved with mixed case
   - When `get_store("walmart")` and `get_store("WALMART")` are called
   - Then both return the same record

4. **Not Found Returns None**
   - Given a database without "Target"
   - When `get_store("Target")` is called
   - Then `None` is returned

5. **Save Summary Persists All Fields**
   - Given valid session metadata
   - When `save_summary(session_id, text, 2, 1, start, end)` is called
   - Then a record exists in `conversation_summaries` with correct `stores_saved=2`, `stores_retrieved=1`, and non-zero `duration_seconds`

## Metadata
- **Complexity**: Medium
- **Labels**: database, sqlite, crud, data-access
- **Required Skills**: Python sqlite3, SQL DML, pytest tmp_path, datetime arithmetic
