# Task: LangChain Agent Core

## Description
Implement `store_assistant/agent/agent.py` with the LangChain `ChatOpenAI` model, tool binding, agent executor, conversation memory, and the `chat()` function that processes a single user turn and returns the agent response with updated history.

## Background
The agent uses the `create_tool_calling_agent` + `AgentExecutor` pattern from LangChain. It maintains conversation history via `MessagesPlaceholder` (passed explicitly as a list, not via `ConversationBufferMemory` object) for compatibility with Gradio's history format. The `chat()` function is the single entry point consumed by the UI.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See the full "agent/agent.py" section under Components and Interfaces.

## Technical Requirements
1. Use `ChatOpenAI(model="gpt-4o-mini")` initialized with `OPENAI_API_KEY` from config
2. Bind tools: `[save_store, retrieve_store]`
3. Use `create_tool_calling_agent(llm, tools, prompt_template)` from `langchain.agents`
4. Wrap with `AgentExecutor(agent=agent, tools=tools, verbose=False)`
5. `chat(user_message: str, history: list[dict]) -> tuple[str, list[dict]]`:
   - Converts `history` list to LangChain message format
   - Invokes `agent_executor.invoke({"input": user_message, "history": lc_history})`
   - Returns `(response_text, updated_history)` where `updated_history` appends the new human/AI turn pair
6. History format: list of `{"role": "human"|"assistant", "content": "..."}` dicts
7. Write basic tests in `store_assistant/tests/test_agent_flow.py` using mocked LLM

## Dependencies
- Step 4 tools (`save_store`, `retrieve_store`) must be complete
- Step 5 task-01 (system prompt) must be complete

## Implementation Approach
1. At module level: instantiate `llm`, create `agent`, create `agent_executor`
2. In `chat()`: convert history dicts to `HumanMessage`/`AIMessage` objects for `MessagesPlaceholder`
3. Extract `response["output"]` as the response text
4. Append `{"role": "human", "content": user_message}` and `{"role": "assistant", "content": response_text}` to history
5. Mock the `AgentExecutor.invoke` in tests to avoid live API calls

## Acceptance Criteria

1. **chat() Returns Response and Updated History**
   - Given a mocked agent executor returning `{"output": "Store saved."}`
   - When `chat("Save Walmart", [])` is called
   - Then the return is `("Store saved.", [{"role": "human", "content": "Save Walmart"}, {"role": "assistant", "content": "Store saved."}])`

2. **History Grows Across Turns**
   - Given an existing history with 1 turn (2 messages)
   - When `chat("another message", history)` is called
   - Then the returned history has 4 messages (2 original + 2 new)

3. **Agent Executor Is Called With Correct Keys**
   - Given a mocked agent executor
   - When `chat("test", [])` is called
   - Then the mock is called with `{"input": "test", "history": []}` (or equivalent LangChain message list)

4. **Module-Level Objects Are Initialized**
   - Given `store_assistant.agent.agent` is imported
   - When checking module attributes
   - Then `llm`, `agent_executor` exist as module-level attributes

## Metadata
- **Complexity**: Medium
- **Labels**: langchain, agent, chatOpenAI, tool-calling, conversation-history
- **Required Skills**: LangChain agents, ChatOpenAI, AgentExecutor, pytest-mock
