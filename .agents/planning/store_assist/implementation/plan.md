# Implementation Plan — Store Assistant

## Implementation Checklist

- [ ] Step 1: Project scaffold, config, and pipenv setup
- [ ] Step 2: Database layer with schema and CRUD
- [ ] Step 3: Phone validation utility
- [ ] Step 4: LangChain tools (save_store, retrieve_store)
- [ ] Step 5: LangChain agent with system prompt and tool binding
- [ ] Step 6: Session state management and termination logic
- [ ] Step 7: Conversation summary generation and persistence
- [ ] Step 8: Gradio UI integration
- [ ] Step 9: LangSmith tracing wiring
- [ ] Step 10: Full test suite

---

## Step 1: Project Scaffold, Config, and Pipenv Setup

### Objective
Create the full modular directory structure, `Pipfile` with all dependencies, and a `config.py` that loads all required environment variables from `.env`.

### Implementation Guidance
- Create the directory tree:
  ```
  store_assistant/
  ├── agent/__init__.py
  ├── db/__init__.py
  ├── ui/__init__.py
  ├── tests/__init__.py
  └── config.py
  main.py
  Pipfile
  .env.example
  ```
- `Pipfile` must pin Python 3.10 and include: `langchain`, `langchain-openai`, `langsmith`, `gradio`, `python-dotenv`, `pytest`
- `config.py` loads: `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2`, `LANGCHAIN_PROJECT`, `STORE_LOOKUP_PASSPHRASE` — raise `ValueError` if required keys are missing
- Create `.env.example` with placeholder values and comments (do not populate `.env`)

### Test Requirements
- Test that `config.py` raises `ValueError` when a required env var is missing (mock env with `monkeypatch`)
- Test that all expected keys are loaded when env is fully populated

### Integration
- Foundation for all subsequent steps; no business logic yet

### Demo
Running `pipenv run python -c "from store_assistant.config import config; print(config)"` prints the loaded config without errors (given a valid `.env`).

---

## Step 2: Database Layer with Schema and CRUD

### Objective
Implement `db/database.py` with SQLite connection management, schema initialization, and all CRUD operations for stores and conversation summaries.

### Implementation Guidance
- `init_db(db_path)` — creates both tables if they don't exist (see schema in detailed design)
- `upsert_store(name, phone)` — INSERT OR REPLACE using `COLLATE NOCASE` on the `name` column
- `get_store(name)` — SELECT with `WHERE LOWER(name) = LOWER(?)`, return `dict` or `None`
- `save_summary(session_id, summary_text, stores_saved, stores_retrieved, session_start, session_end)` — INSERT into `conversation_summaries`
- Use a context manager (`with sqlite3.connect(db_path) as conn`) for all operations
- Default `db_path` comes from `config.py` (e.g. `STORE_DB_PATH`, defaulting to `store_assistant.db`)

### Test Requirements
- `test_database.py`:
  - Insert a store and verify it can be retrieved
  - Upsert same store name with new phone, verify phone is updated
  - Case-insensitive get: save "Walmart", retrieve with "walmart" — should match
  - Get non-existent store returns `None`
  - Save summary and verify it is persisted with correct metadata
- Use `tmp_path` pytest fixture for isolated DB files

### Integration
- Builds on Step 1 config; consumed by tools in Step 4

### Demo
Running `pytest tests/test_database.py` passes all tests with isolated temp DB.

---

## Step 3: Phone Validation Utility

### Objective
Implement a `validate_phone(phone: str) -> bool` utility function and a `normalize_phone(phone: str) -> str` function that standardizes accepted US formats.

### Implementation Guidance
- Place in `agent/tools.py` (or a shared `agent/utils.py`)
- Accepted patterns (all should normalize to digits-only or E.164):
  - `(555) 555-5555`
  - `555-555-5555`
  - `5555555555`
  - `+15555555555`
- Use a single regex that strips formatting characters then checks for 10 digits (or 11 with leading `1`)
- `normalize_phone` strips all non-digit characters, returns 10-digit string (strips leading `1` if 11 digits starting with `1`)

### Test Requirements
- `test_phone_validation.py`:
  - Valid: `(555) 555-5555`, `555-555-5555`, `5555555555`, `+15555555555`, `555.555.5555`
  - Invalid: `123`, `abcdefghij`, `12345678901234`, empty string, `555-55-555`
  - Normalization: `(555) 555-5555` → `5555555555`

### Integration
- Used by `save_store` tool in Step 4

### Demo
Running `pytest tests/test_phone_validation.py` passes all valid/invalid cases.

---

## Step 4: LangChain Tools — save_store and retrieve_store

### Objective
Implement two LangChain `@tool`-decorated functions: `save_store` and `retrieve_store`, wiring phone validation and DB operations.

### Implementation Guidance
- `save_store(name: str, phone: str) -> str`:
  - Call `validate_phone(phone)` — if invalid, return an error string describing valid formats
  - Call `db.upsert_store(name, normalize_phone(phone))`
  - Return success confirmation string
- `retrieve_store(name: str, passphrase: str) -> str`:
  - Compare `passphrase` against `config.STORE_LOOKUP_PASSPHRASE` (case-sensitive)
  - If wrong, return a "wrong passphrase" error string
  - If correct, call `db.get_store(name)`
  - Return phone number string or "store not found" message
- Passphrase retry logic (up to 3 attempts) is managed by the agent in Step 5, not within the tool itself — the tool simply returns success/failure on each call
- Both tools must have clear docstrings as LangChain uses them for tool selection

### Test Requirements
- `test_passphrase.py`:
  - Correct passphrase + existing store → returns phone
  - Wrong passphrase → returns wrong passphrase message
  - Correct passphrase + non-existent store → returns not found message
- Use `monkeypatch` to set `STORE_LOOKUP_PASSPHRASE` and a temp DB

### Integration
- Builds on Steps 2 and 3; consumed by agent in Step 5

### Demo
Calling `save_store("Walmart", "555-123-4567")` and `retrieve_store("walmart", correct_passphrase)` directly in a Python REPL returns expected strings.

---

## Step 5: LangChain Agent with System Prompt and Tool Binding

### Objective
Implement `agent/agent.py` with the LangChain `ChatOpenAI` model, tool binding, system prompt, and a stateful `chat()` function that processes one user turn.

### Implementation Guidance
- Use `ChatOpenAI(model="gpt-4o-mini")` with tools bound via `.bind_tools([save_store, retrieve_store])`
- Use `create_tool_calling_agent` + `AgentExecutor` pattern
- System prompt (in `agent/prompts.py`) must instruct the agent:
  - It is a store directory assistant
  - It can only save and look up stores
  - It must validate phone formats before saving
  - It must request the passphrase before any lookup
  - It must politely redirect off-topic messages
  - It must recognize farewell intent ("I'm done", "I'm good", "goodbye", etc.)
  - It must never reveal or discuss the passphrase value
- Use `ConversationBufferMemory` (or `MessagesPlaceholder`) for multi-turn history
- `chat(user_message: str, history: list) -> tuple[str, list]` — invokes the agent and returns the response and updated history

### Test Requirements
- `test_agent_flow.py` (mock LLM):
  - Mock LLM response for a save-store turn; verify `save_store` tool is called
  - Mock LLM response for a retrieve-store turn; verify `retrieve_store` tool is called
  - Verify history grows correctly across turns

### Integration
- Builds on Steps 3 and 4; extended in Steps 6 and 7; consumed by UI in Step 8

### Demo
Running a two-turn conversation in a Python script (save a store, then retrieve it) produces correct agent responses.

---

## Step 6: Session State Management and Termination Logic

### Objective
Add session state tracking to the agent: off-topic counter, stores saved/retrieved counts, session start time, passphrase retry counter, and both termination conditions.

### Implementation Guidance
- Wrap agent state in a `SessionState` dataclass:
  ```python
  @dataclass
  class SessionState:
      session_id: str          # uuid4
      session_start: datetime
      off_topic_count: int = 0
      passphrase_attempts: int = 0
      stores_saved: int = 0
      stores_retrieved: int = 0
      terminated: bool = False
      termination_reason: str = ""
  ```
- Before invoking the agent, check `state.terminated` — if True, return a "session ended" message
- After each agent response, inspect the response to determine:
  - Was it a successful save? Increment `stores_saved`, reset `off_topic_count`
  - Was it a successful retrieve? Increment `stores_retrieved`, reset `off_topic_count`
  - Was it a farewell termination? Set `terminated = True`, `termination_reason = "farewell"`
  - Was it an off-topic redirect? Increment `off_topic_count`; if `off_topic_count >= 3`, set `terminated = True`, `termination_reason = "off_topic"`
  - Was it a passphrase failure? Increment `passphrase_attempts`; if `>= 3`, reset and drop request
- Use a sentinel string or structured output from the agent/tools to signal these events reliably

### Test Requirements
- `test_offtopic_termination.py`:
  - 1 off-topic message → warning response, `off_topic_count = 1`, not terminated
  - 2 off-topic messages → warning, `off_topic_count = 2`, not terminated
  - 3 off-topic messages → termination message, `terminated = True`
  - In-scope message resets `off_topic_count` to 0
- Mock LLM responses to simulate off-topic classification

### Integration
- Extends Step 5 agent; session state passed to Step 7 summary generation

### Demo
Sending 3 consecutive off-topic messages via the agent terminates the session with a goodbye message.

---

## Step 7: Conversation Summary Generation and Persistence

### Objective
On session termination, use the LLM to generate a rich narrative summary of the conversation, then persist it to the DB with full metadata.

### Implementation Guidance
- Triggered whenever `state.terminated` transitions to `True`
- Build a summary prompt including:
  - Full conversation history (human + AI turns)
  - Session metadata (stores saved count, stores retrieved count)
  - Instruction to write a concise narrative paragraph
- Call `ChatOpenAI` directly (not through the tool-calling agent) to generate the summary text
- Call `db.save_summary(session_id, summary_text, stores_saved, stores_retrieved, session_start, session_end)`
- Return the summary text as part of the final agent response to the user
- `session_end = datetime.utcnow()`, `duration_seconds = (session_end - session_start).total_seconds()`

### Test Requirements
- In `test_agent_flow.py`:
  - Mock LLM for summary generation; verify `db.save_summary` is called with correct args on farewell termination
  - Verify summary record exists in DB after termination

### Integration
- Builds on Steps 5 and 6; completes the full conversation lifecycle

### Demo
After saying "I'm done", the agent returns a farewell message with a summary paragraph, and the `conversation_summaries` table contains a new record.

---

## Step 8: Gradio UI Integration

### Objective
Implement `ui/app.py` with a Gradio `ChatInterface` that wires to the agent's `chat()` function and launches a local web UI.

### Implementation Guidance
- Use `gr.ChatInterface(fn=agent_chat_fn)` where `agent_chat_fn(message, history)` wraps `agent.chat()`
- Initialize a single `SessionState` per Gradio session using Gradio's `gr.State`
- Display agent responses in the chat window
- Add a title and brief description to the interface
- `main.py` at the project root: imports `ui.app` and calls `app.launch()`
- After session termination, the chat input should be disabled or the agent should respond with "session ended" to further messages

### Test Requirements
- No automated UI tests required; manual smoke test is sufficient
- Verify `pytest` still passes all existing tests after wiring

### Integration
- Consumes the complete agent from Steps 5–7; exposes the full application

### Demo
Running `pipenv run python main.py` opens `http://localhost:7860` with a working chat interface where the full save/retrieve/terminate flow can be demonstrated.

---

## Step 9: LangSmith Tracing Wiring

### Objective
Ensure all LLM calls are traced to LangSmith by configuring the required environment variables and verifying traces appear in the LangSmith dashboard.

### Implementation Guidance
- In `config.py`, set:
  ```python
  os.environ["LANGCHAIN_TRACING_V2"] = "true"
  os.environ["LANGCHAIN_API_KEY"] = config.LANGCHAIN_API_KEY
  os.environ["LANGCHAIN_PROJECT"] = config.LANGCHAIN_PROJECT  # "store-assistant"
  ```
- These must be set before any LangChain objects are instantiated
- Add `LANGCHAIN_API_KEY` and `LANGCHAIN_PROJECT` to `.env.example`
- Verify in `config.py` that `LANGCHAIN_API_KEY` is present; raise `ValueError` if missing
- LangSmith tracing is automatic once env vars are set — no additional code required

### Test Requirements
- Update `test_config.py` (from Step 1) to verify `LANGCHAIN_API_KEY` is validated
- No LangSmith-specific automated tests (external service); manual verification via dashboard

### Integration
- Extends Step 1 config; applies globally to all agent LLM calls

### Demo
After running a conversation, traces appear in the LangSmith project dashboard at `smith.langchain.com`.

---

## Step 10: Full Test Suite — Final Wiring and Coverage

### Objective
Ensure all five test files are complete, all tests pass, and the full application runs end-to-end.

### Implementation Guidance
- Run `pipenv run pytest tests/ -v` — all tests must pass
- Ensure test isolation: all DB tests use `tmp_path`, all LLM tests mock the OpenAI client
- Add a `conftest.py` with shared fixtures: temp DB path, mock LLM, mock config
- Review test coverage across all five files:
  - `test_phone_validation.py` — valid/invalid phone formats, normalization
  - `test_database.py` — upsert, case-insensitive get, not-found, save summary
  - `test_passphrase.py` — correct/wrong passphrase, 3-attempt drop
  - `test_agent_flow.py` — save turn, retrieve turn, summary on termination
  - `test_offtopic_termination.py` — 1/2/3 off-topic strikes, reset on in-scope
- Verify `pipenv run python main.py` launches Gradio cleanly

### Test Requirements
- All tests pass with `pytest tests/ -v`
- No test makes live API calls to OpenAI or LangSmith

### Integration
- Final step; validates the complete system end-to-end

### Demo
`pytest tests/ -v` shows all tests green. `python main.py` launches the Gradio UI and a full save → retrieve → "I'm done" conversation works correctly with a summary saved to the DB.
