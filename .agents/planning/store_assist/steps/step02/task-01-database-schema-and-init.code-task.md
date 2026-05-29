# Task: Database Schema and Initialization

## Description
Implement `store_assistant/db/database.py` with SQLite connection management and schema initialization. Create both the `stores` and `conversation_summaries` tables with proper constraints, and expose an `init_db()` function that is idempotent (safe to call multiple times).

## Background
The project uses SQLite as a file-based database. Two tables are required: `stores` for store records and `conversation_summaries` for end-of-session summaries. The database module is shared by the agent tools and the summary persistence logic. All connections use context managers to ensure proper cleanup.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See the "Data Models" and "db/database.py" sections for exact schema DDL.

## Technical Requirements
1. `init_db(db_path: str) -> None` — creates both tables using `CREATE TABLE IF NOT EXISTS`
2. `stores` table: `id`, `name TEXT UNIQUE COLLATE NOCASE`, `phone TEXT`, `created_at`, `updated_at`
3. `conversation_summaries` table: `id`, `session_id TEXT`, `summary_text TEXT`, `stores_saved INT`, `stores_retrieved INT`, `session_start TIMESTAMP`, `session_end TIMESTAMP`, `duration_seconds REAL`, `created_at`
4. Use `sqlite3` from stdlib only (no ORM)
5. All DB operations use `with sqlite3.connect(db_path) as conn:` context manager
6. `db_path` defaults to `config.store_db_path` when not explicitly provided

## Dependencies
- Step 1 (config) must be complete — `config.store_db_path` must be available

## Implementation Approach
1. Import `sqlite3`, `datetime`, and `config` from `store_assistant.config`
2. Define `STORES_DDL` and `SUMMARIES_DDL` as module-level string constants
3. Implement `init_db(db_path=None)` that opens a connection and executes both DDL statements
4. Call `conn.execute("PRAGMA journal_mode=WAL")` for better concurrent write safety
5. Write tests in `store_assistant/tests/test_database.py` using `tmp_path` fixture

## Acceptance Criteria

1. **Tables Created on init_db Call**
   - Given a new empty SQLite file path
   - When `init_db(db_path)` is called
   - Then both `stores` and `conversation_summaries` tables exist in the database

2. **init_db Is Idempotent**
   - Given a database with already-created tables
   - When `init_db(db_path)` is called again
   - Then no error is raised and tables remain intact

3. **stores Table Has NOCASE Constraint**
   - Given the `stores` table schema
   - When inspecting the `name` column
   - Then it has `COLLATE NOCASE` and `UNIQUE` constraints

4. **Context Manager Used**
   - Given the implementation
   - When reviewing `database.py`
   - Then all sqlite3 calls use `with sqlite3.connect(...) as conn:` pattern

## Metadata
- **Complexity**: Low
- **Labels**: database, sqlite, schema, setup
- **Required Skills**: Python sqlite3, SQL DDL, pytest tmp_path
