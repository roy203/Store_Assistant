# Task: Config and Environment Loading

## Description
Implement `store_assistant/config.py` to load all required environment variables from `.env` using `python-dotenv`, expose them as a typed config object, set LangSmith environment variables, and raise `ValueError` for any missing required keys. Also create `.env.example` with documented placeholders.

## Background
All secrets and configuration (OpenAI key, LangSmith key, passphrase) must come from `.env` and never be hardcoded. The config module is imported by every other module, so it must be robust. LangSmith tracing requires specific env vars to be set before any LangChain objects are instantiated, making config the right place to set them.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See the "config.py" section under Components and Interfaces, and the NFR requirements NFR-01 through NFR-05.

## Technical Requirements
1. Use `python-dotenv` `load_dotenv()` to load `.env` from the project root
2. Required keys that MUST raise `ValueError` if missing: `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`, `STORE_LOOKUP_PASSPHRASE`
3. Optional keys with defaults: `LANGCHAIN_TRACING_V2` (default `"true"`), `LANGCHAIN_PROJECT` (default `"store-assistant"`), `STORE_DB_PATH` (default `"store_assistant.db"`)
4. After loading, set `os.environ["LANGCHAIN_TRACING_V2"]`, `os.environ["LANGCHAIN_API_KEY"]`, `os.environ["LANGCHAIN_PROJECT"]` so LangChain picks them up automatically
5. Expose a single `Config` dataclass instance named `config` at module level
6. Create `.env.example` with all keys, placeholder values, and inline comments explaining each
7. Write tests in `store_assistant/tests/test_config.py`

## Dependencies
- Tasks 01 and 02 must be complete
- `python-dotenv` must be in `Pipfile`

## Implementation Approach
1. Define a `Config` dataclass with all fields typed
2. Implement a `_load_config()` function that calls `load_dotenv()`, reads `os.environ`, validates required keys, and returns a `Config` instance
3. Call `_load_config()` at module level: `config = _load_config()`
4. After creating the config, set the three LangSmith `os.environ` keys
5. Create `.env.example` listing: `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2`, `LANGCHAIN_PROJECT`, `STORE_LOOKUP_PASSPHRASE`, `STORE_DB_PATH`

## Acceptance Criteria

1. **Missing Required Key Raises ValueError**
   - Given an environment missing `OPENAI_API_KEY`
   - When `store_assistant.config` is imported (or `_load_config()` is called with monkeypatched env)
   - Then a `ValueError` is raised with a descriptive message naming the missing key

2. **All Keys Loaded Successfully**
   - Given a fully populated environment with all required keys
   - When `config` is accessed
   - Then all fields (`openai_api_key`, `langchain_api_key`, `store_lookup_passphrase`, `store_db_path`, `langchain_project`) are populated with correct values

3. **LangSmith Env Vars Set**
   - Given a valid config loaded
   - When checking `os.environ`
   - Then `LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`, and `LANGCHAIN_PROJECT` are set

4. **Env Example File Exists**
   - Given the project root
   - When reading `.env.example`
   - Then all six config keys are present with placeholder values and comments

5. **Optional Keys Use Defaults**
   - Given an environment with only the three required keys set
   - When config is loaded
   - Then `store_db_path` defaults to `"store_assistant.db"` and `langchain_project` defaults to `"store-assistant"`

## Metadata
- **Complexity**: Low
- **Labels**: config, environment, security, langsmith, setup
- **Required Skills**: Python dataclasses, python-dotenv, environment variables, pytest monkeypatch
