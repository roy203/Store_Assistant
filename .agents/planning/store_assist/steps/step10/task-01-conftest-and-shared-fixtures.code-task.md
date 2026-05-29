# Task: conftest.py and Shared Test Fixtures

## Description
Create `store_assistant/tests/conftest.py` with shared pytest fixtures used across all test files: a temp DB path, a mock LLM, and a mock config. This eliminates duplication across the five test files and ensures consistent test isolation.

## Background
Five test files share common needs: a temporary SQLite database (using `tmp_path`), a mocked `ChatOpenAI` instance to avoid live API calls, and a patched config with test values for passphrase, DB path, and API keys. Centralizing these in `conftest.py` keeps tests DRY.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See the Testing Strategy section.

## Technical Requirements
1. Create `store_assistant/tests/conftest.py`
2. `temp_db` fixture (scope `function`): creates a temp SQLite DB via `tmp_path`, calls `init_db()`, yields the path, cleans up
3. `mock_llm` fixture: returns a `MagicMock` that mimics `ChatOpenAI` with a configurable `.invoke()` return value
4. `mock_config` fixture: uses `monkeypatch` to set all required env vars to test values (`STORE_LOOKUP_PASSPHRASE="testpass"`, `OPENAI_API_KEY="test-key"`, `LANGCHAIN_API_KEY="test-lc-key"`, etc.)
5. All fixtures must be usable by any test file via pytest's conftest discovery

## Dependencies
- Step 2 (`init_db`) must be complete

## Implementation Approach
1. Import `pytest`, `init_db`, `sqlite3`
2. Define `@pytest.fixture def temp_db(tmp_path)` that returns a string path to an initialized DB
3. Define `@pytest.fixture def mock_llm(mocker)` using `pytest-mock` that patches `ChatOpenAI`
4. Define `@pytest.fixture def mock_config(monkeypatch)` that patches all required env vars and reloads config

## Acceptance Criteria

1. **temp_db Fixture Provides Initialized DB**
   - Given a test using `temp_db` fixture
   - When the fixture is injected
   - Then the path points to a SQLite file with both tables created

2. **mock_llm Returns Configurable Response**
   - Given `mock_llm` fixture with `mock_llm.invoke.return_value.content = "test response"`
   - When `mock_llm.invoke(...)` is called in a test
   - Then `"test response"` is returned

3. **mock_config Sets All Required Env Vars**
   - Given a test using `mock_config`
   - When `os.environ["STORE_LOOKUP_PASSPHRASE"]` is checked
   - Then `"testpass"` is returned

4. **Fixtures Are Available to All Test Files**
   - Given `conftest.py` in the `tests/` directory
   - When any test file requests `temp_db`, `mock_llm`, or `mock_config`
   - Then pytest injects them without additional imports

## Metadata
- **Complexity**: Low
- **Labels**: testing, fixtures, conftest, pytest
- **Required Skills**: pytest fixtures, pytest-mock, monkeypatch
