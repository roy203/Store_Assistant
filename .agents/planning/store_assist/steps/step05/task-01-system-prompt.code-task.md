# Task: Agent System Prompt

## Description
Implement `store_assistant/agent/prompts.py` containing the system prompt template that governs the agent's behavior: scope, tool usage instructions, phone validation guidance, passphrase handling, off-topic redirection, and farewell detection.

## Background
LangChain tool-calling agents are guided by a system prompt. The system prompt must be comprehensive enough to instruct the agent to handle all conversation scenarios: saving stores, retrieving stores (with passphrase), redirecting off-topic messages, and recognizing farewells. It must also include a `{history}` placeholder for `MessagesPlaceholder`.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See the "agent/agent.py" section and all functional requirements FR-01 through FR-14.

## Technical Requirements
1. Create `store_assistant/agent/prompts.py`
2. Define `SYSTEM_PROMPT` as a string constant with a detailed system message
3. The prompt MUST instruct the agent to:
   - Only help with saving and looking up stores
   - Ask for store name and phone when saving; validate phone format before calling `save_store`
   - Ask for store name, then request passphrase before calling `retrieve_store`
   - Never reveal or hint at the passphrase value
   - Politely redirect off-topic messages with: `"[OFF_TOPIC]"` prefix in its response (sentinel for termination counting)
   - Recognize farewell utterances and respond with: `"[FAREWELL]"` prefix
   - Recognize `"WRONG_PASSPHRASE"` tool output and prompt the user to try again
   - Recognize `"STORE_NOT_FOUND"` tool output and inform the user
4. Define a `ChatPromptTemplate` combining the system message and `MessagesPlaceholder(variable_name="history")`

## Dependencies
- Step 1 scaffold must be complete

## Implementation Approach
1. Write `SYSTEM_PROMPT` as a multi-line string covering all scenarios
2. Use `ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), MessagesPlaceholder("history"), ("human", "{input}")])` pattern
3. Export both `SYSTEM_PROMPT` and `prompt_template` from the module

## Acceptance Criteria

1. **Prompt Contains All Required Instructions**
   - Given `SYSTEM_PROMPT`
   - When reviewing its content
   - Then it covers: scope restriction, save flow, retrieve flow, passphrase handling, off-topic sentinel `[OFF_TOPIC]`, farewell sentinel `[FAREWELL]`, and tool output handling

2. **Prompt Template Is Valid LangChain Object**
   - Given `prompt_template` from `agent/prompts.py`
   - When calling `prompt_template.input_variables`
   - Then it includes `"history"` and `"input"`

3. **Sentinel Strings Are Documented**
   - Given `prompts.py`
   - When reviewing the file
   - Then `[OFF_TOPIC]` and `[FAREWELL]` sentinel strings are defined as constants and referenced in the prompt

## Metadata
- **Complexity**: Medium
- **Labels**: langchain, prompt-engineering, agent, system-prompt
- **Required Skills**: LangChain prompt templates, prompt engineering
