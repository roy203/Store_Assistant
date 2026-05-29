# Task: save_store LangChain Tool

## Description
Implement the `save_store` LangChain `@tool`-decorated function in `store_assistant/agent/tools.py`. This tool validates the phone number, normalizes it, and upserts the store record to SQLite, returning a user-facing confirmation or error string.

## Background
LangChain tool-calling agents select tools based on their docstrings. The `save_store` tool must have a clear, descriptive docstring and well-typed arguments. Phone validation happens here before DB write. The tool returns a plain string that the agent will relay to the user.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See FR-01 through FR-05 and the "agent/tools.py" section under Components and Interfaces.

## Technical Requirements
1. Decorate with `@tool` from `langchain_core.tools`
2. Function signature: `save_store(name: str, phone: str) -> str`
3. Docstring must clearly describe when to use this tool (LangChain uses it for tool selection)
4. Call `validate_phone(phone)` — if invalid, return a string explaining valid US formats
5. Call `normalize_phone(phone)` on valid input before passing to DB
6. Call `db.upsert_store(name, normalized_phone)`
7. Return a success confirmation string including the store name and formatted phone

## Dependencies
- Step 2 (`db/database.py` CRUD) must be complete
- Step 3 (phone validation utils) must be complete

## Implementation Approach
1. Import `tool` from `langchain_core.tools`, `validate_phone` and `normalize_phone` from `agent/utils.py`, and `upsert_store` from `db/database.py`
2. Write a docstring that says: "Use this tool to save a store's name and phone number to the database."
3. Implement validation branch: if invalid, return `"Invalid phone number. Please provide a US phone number in one of these formats: (555) 555-5555, 555-555-5555, 5555555555, +15555555555"`
4. On success, return `f"Store '{name}' has been saved with phone number {normalized_phone}."`

## Acceptance Criteria

1. **Valid Phone Triggers DB Upsert**
   - Given `save_store("Walmart", "555-123-4567")` is called with a valid phone
   - When the function executes
   - Then `upsert_store` is called and a success confirmation string is returned

2. **Invalid Phone Returns Error String**
   - Given `save_store("Walmart", "123")` is called with an invalid phone
   - When the function executes
   - Then a descriptive error string is returned and `upsert_store` is NOT called

3. **Returned String Contains Store Name**
   - Given a successful save
   - When the return value is inspected
   - Then the string contains the store name

4. **Tool Is Decorated Correctly**
   - Given the `save_store` function
   - When checking its type
   - Then it is a LangChain `StructuredTool` (result of `@tool` decorator)

5. **Tool Has Descriptive Docstring**
   - Given the `save_store` tool
   - When accessing `.description`
   - Then a non-empty descriptive string is returned

## Metadata
- **Complexity**: Low
- **Labels**: langchain, tools, agent, save, validation
- **Required Skills**: LangChain tools API, Python, pytest-mock
