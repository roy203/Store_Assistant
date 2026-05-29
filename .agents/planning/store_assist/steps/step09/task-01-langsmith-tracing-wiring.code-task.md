# Task: LangSmith Tracing Wiring

## Description
Ensure LangSmith tracing is correctly wired by verifying `config.py` sets the required LangSmith environment variables before any LangChain objects are instantiated, and confirm via the LangSmith dashboard that traces are captured after a live conversation.

## Background
LangChain automatically sends traces to LangSmith when `LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_API_KEY`, and `LANGCHAIN_PROJECT` are set as environment variables before any LangChain object is created. This was partially set up in Step 1 (config.py). This step verifies the wiring is correct and complete, confirms import order is safe, and validates tracing end-to-end.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See Step 9 implementation guidance and NFR-01.

## Technical Requirements
1. Verify `config.py` sets `os.environ["LANGCHAIN_TRACING_V2"]`, `os.environ["LANGCHAIN_API_KEY"]`, and `os.environ["LANGCHAIN_PROJECT"]` at module load time (before any LangChain import)
2. Ensure `config` is the first import in `agent/agent.py` (before `langchain` imports) so env vars are set before LangChain initializes
3. Verify `.env.example` includes `LANGCHAIN_API_KEY` and `LANGCHAIN_PROJECT` with comments
4. Update `test_config.py` to assert `LANGCHAIN_API_KEY` validation is present (raises `ValueError` if missing)
5. No new runtime code required — this is a verification and wiring correctness task

## Dependencies
- Step 1 (`config.py`) must be complete
- Step 5 (`agent.py`) must be complete
- A valid `LANGCHAIN_API_KEY` in `.env` is required for manual dashboard verification

## Implementation Approach
1. Review `config.py`: confirm the three `os.environ` assignments exist after `Config` is instantiated
2. Review `agent/agent.py`: confirm `from store_assistant.config import config` is the first import
3. If either is missing, add the missing piece
4. Update `test_config.py`: add test that importing config without `LANGCHAIN_API_KEY` raises `ValueError`
5. Manual verification: run `python main.py`, perform one save + one retrieve, check LangSmith dashboard at `smith.langchain.com` for the `store-assistant` project

## Acceptance Criteria

1. **LangSmith Env Vars Set Before LangChain Imports**
   - Given `store_assistant/config.py`
   - When the module is imported
   - Then `os.environ["LANGCHAIN_TRACING_V2"]`, `os.environ["LANGCHAIN_API_KEY"]`, `os.environ["LANGCHAIN_PROJECT"]` are all set

2. **Config Is First Import in agent.py**
   - Given `store_assistant/agent/agent.py`
   - When reviewing import order
   - Then `from store_assistant.config import config` appears before any `langchain` imports

3. **Missing LANGCHAIN_API_KEY Raises ValueError**
   - Given an environment without `LANGCHAIN_API_KEY`
   - When `config.py` is loaded
   - Then `ValueError` is raised

4. **Traces Appear in LangSmith Dashboard (Manual)**
   - Given a running app with valid `LANGCHAIN_API_KEY`
   - When a save + retrieve conversation is completed
   - Then traces appear in the `store-assistant` LangSmith project (manual verification)

## Metadata
- **Complexity**: Low
- **Labels**: langsmith, tracing, observability, configuration
- **Required Skills**: LangSmith, environment variables, Python import ordering
