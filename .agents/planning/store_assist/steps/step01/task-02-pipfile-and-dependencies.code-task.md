# Task: Pipfile and Dependencies

## Description
Create the `Pipfile` that defines the Python 3.10.17 environment and all runtime and development dependencies for the Store Assistant project. This ensures a reproducible environment via `pipenv`.

## Background
The project uses `pipenv` with Python 3.10.17 as the local environment manager. All dependencies must be pinned to compatible versions. The runtime stack is LangChain + OpenAI, Gradio for UI, SQLite (stdlib), python-dotenv for config, and LangSmith for tracing. pytest is the test runner.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See "Technology Choices" appendix for the full stack.

## Technical Requirements
1. `Pipfile` must specify `python_version = "3.10"`
2. Runtime packages (`[packages]`): `langchain`, `langchain-openai`, `langsmith`, `gradio`, `python-dotenv`
3. Development packages (`[dev-packages]`): `pytest`, `pytest-mock`
4. Pin versions compatible with Python 3.10 — use recent stable versions
5. Do NOT run `pipenv install` — only create the `Pipfile`

## Dependencies
- Task 01 (directory scaffold) must be complete

## Implementation Approach
1. Create `Pipfile` at the project root with `[requires]`, `[packages]`, and `[dev-packages]` sections
2. Use `"*"` or specific version constraints for each package
3. Ensure `langchain-openai` is included separately from `langchain` (required for `ChatOpenAI`)

## Acceptance Criteria

1. **Pipfile Exists at Root**
   - Given the project root
   - When checking for `Pipfile`
   - Then `Pipfile` exists with all three sections: `[requires]`, `[packages]`, `[dev-packages]`

2. **All Runtime Dependencies Present**
   - Given the `[packages]` section
   - When checking package names
   - Then `langchain`, `langchain-openai`, `langsmith`, `gradio`, `python-dotenv` are all listed

3. **Dev Dependencies Present**
   - Given the `[dev-packages]` section
   - When checking package names
   - Then `pytest` and `pytest-mock` are listed

4. **Python Version Correct**
   - Given the `[requires]` section
   - When reading `python_version`
   - Then it equals `"3.10"`

## Metadata
- **Complexity**: Low
- **Labels**: setup, dependencies, pipenv, environment
- **Required Skills**: Python packaging, pipenv
