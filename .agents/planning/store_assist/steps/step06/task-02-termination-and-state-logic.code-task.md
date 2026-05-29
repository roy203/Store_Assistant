# Task: Termination and Session State Logic

## Description
Extend `store_assistant/agent/agent.py` to integrate `SessionState` into the `chat()` function. Implement all state-mutation logic: detecting off-topic responses, farewell termination, successful save/retrieve counting, and passphrase retry tracking. The `chat()` function signature changes to accept and return `SessionState`.

## Background
After each agent response, the response text must be inspected for sentinel strings (`[OFF_TOPIC]`, `[FAREWELL]`, `WRONG_PASSPHRASE` tool output relayed by the agent) to update the session state. Termination conditions: 3 consecutive off-topic messages, or any farewell. The `chat()` function must short-circuit if the session is already terminated.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See Step 6 and the full error handling table.

## Technical Requirements
1. Update `chat(user_message, history, state: SessionState) -> tuple[str, list, SessionState]`
2. If `state.terminated`: return `("This session has ended. Please refresh to start a new conversation.", history, state)` immediately
3. After getting agent response, inspect `response_text` for:
   - Contains `"[OFF_TOPIC]"` → increment `state.off_topic_count`; if `>= 3` set `state.terminated = True`, `state.termination_reason = "off_topic"`; else warn user (the agent's message already contains the warning)
   - Contains `"[FAREWELL]"` → set `state.terminated = True`, `state.termination_reason = "farewell"`
   - Contains `"Store saved"` or `"has been saved"` → increment `state.stores_saved`, reset `state.off_topic_count = 0`
   - Contains `"WRONG_PASSPHRASE"` relayed by agent → increment `state.passphrase_attempts`; if `>= 3` reset `state.passphrase_attempts = 0`
   - Contains `"phone number is"` (successful retrieve) → increment `state.stores_retrieved`, reset `state.off_topic_count = 0`
4. Strip sentinel prefixes from response text before returning to user
5. Write tests in `store_assistant/tests/test_offtopic_termination.py`

## Dependencies
- Step 6 task-01 (`SessionState`) must be complete
- Step 5 task-02 (agent core) must be complete

## Implementation Approach
1. Update `chat()` signature to include `state: SessionState` parameter and return it
2. Add early-return guard for `state.terminated`
3. Implement `_update_state(response_text: str, state: SessionState) -> SessionState` as a pure helper function (easier to test in isolation)
4. Call `_update_state` after every successful agent invocation
5. Clean sentinel strings from response before returning: `response_text.replace("[OFF_TOPIC]", "").replace("[FAREWELL]", "").strip()`

## Acceptance Criteria

1. **Terminated Session Short-Circuits**
   - Given `state.terminated = True`
   - When `chat("any message", [], state)` is called
   - Then agent executor is NOT invoked and a session-ended message is returned

2. **Off-Topic Increments Counter**
   - Given `state.off_topic_count = 0`
   - When agent returns `"[OFF_TOPIC] I can only help with stores."`
   - Then `state.off_topic_count = 1` and `state.terminated = False`

3. **Third Off-Topic Terminates Session**
   - Given `state.off_topic_count = 2`
   - When agent returns another `"[OFF_TOPIC]"` response
   - Then `state.terminated = True` and `state.termination_reason = "off_topic"`

4. **Farewell Terminates Session**
   - Given any session state
   - When agent returns `"[FAREWELL] Goodbye!"`
   - Then `state.terminated = True` and `state.termination_reason = "farewell"`

5. **In-Scope Message Resets Off-Topic Counter**
   - Given `state.off_topic_count = 2`
   - When agent returns a successful save response (no `[OFF_TOPIC]`)
   - Then `state.off_topic_count = 0`

6. **Sentinels Stripped From User-Facing Response**
   - Given agent returns `"[OFF_TOPIC] Sorry, I can only help with stores."`
   - When `chat()` returns
   - Then the returned response string does NOT contain `"[OFF_TOPIC]"`

## Metadata
- **Complexity**: Medium
- **Labels**: session, state-machine, termination, off-topic, farewell
- **Required Skills**: Python, string parsing, state management, pytest-mock
