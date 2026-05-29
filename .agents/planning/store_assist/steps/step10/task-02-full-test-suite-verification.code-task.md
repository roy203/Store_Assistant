# Task: Full Test Suite Verification and Gap Fill

## Description
Audit all five test files for completeness, fill any missing test cases, ensure all tests are isolated (no live API calls), and verify the complete test suite passes with `pytest tests/ -v`. Fix any gaps or broken tests discovered during the audit.

## Background
By Step 10, code for all features exists. This task ensures all test files are complete and correct: `test_config.py`, `test_phone_validation.py`, `test_database.py`, `test_passphrase.py`, `test_agent_flow.py`, and `test_offtopic_termination.py`. Every test must mock external dependencies (OpenAI, LangSmith) and use temp DBs.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See the full Testing Strategy table.

## Technical Requirements
1. All tests must pass with `pipenv run pytest tests/ -v` with zero failures
2. No test may make live calls to OpenAI API or LangSmith (use mocks)
3. All DB-touching tests must use `temp_db` fixture
4. Test coverage required across all six files:
   - `test_config.py`: missing key raises ValueError, defaults applied, LangSmith env vars set
   - `test_phone_validation.py`: all valid formats, all invalid formats, normalization
   - `test_database.py`: insert, upsert, case-insensitive get, not-found, save summary
   - `test_passphrase.py`: correct passphrase, wrong passphrase, store not found
   - `test_agent_flow.py`: save turn, retrieve turn, summary called on termination, summary saved to DB
   - `test_offtopic_termination.py`: 1-strike, 2-strike, 3-strike terminates, reset on in-scope
5. Use `@pytest.mark.parametrize` for phone validation test cases

## Dependencies
- All previous steps (1–9) must be complete

## Implementation Approach
1. Run `pytest tests/ -v` and note any failures or missing tests
2. For each failing test: diagnose root cause and fix either the test or the implementation bug
3. For each missing test case from the plan: add it to the appropriate test file
4. Ensure all mocks are set up correctly (no `MissingEnvironmentVariable` errors during test runs)
5. Final run: `pytest tests/ -v --tb=short` must show all green

## Acceptance Criteria

1. **All Tests Pass**
   - Given the complete codebase
   - When `pipenv run pytest tests/ -v` is run
   - Then all tests pass with zero failures and zero errors

2. **No Live API Calls**
   - Given the test suite
   - When reviewing all test files
   - Then no test imports or calls real `OpenAI` or `LangSmith` clients without mocking

3. **All Five Coverage Areas Met**
   - Given the test suite
   - When reviewing test file contents
   - Then each of the six test files contains tests for all cases listed in the Testing Strategy

4. **Parametrized Phone Tests**
   - Given `test_phone_validation.py`
   - When reviewing the file
   - Then `@pytest.mark.parametrize` is used for valid and invalid phone cases

5. **Full End-to-End Smoke Test**
   - Given the Gradio app launched with `python main.py`
   - When manually running: save "Walmart" with "555-123-4567", retrieve "Walmart" with correct passphrase, say "I'm done"
   - Then store is saved, phone is returned, session terminates with summary, summary exists in DB

## Metadata
- **Complexity**: Medium
- **Labels**: testing, pytest, integration, coverage, smoke-test
- **Required Skills**: pytest, pytest-mock, parametrize, test isolation, debugging
