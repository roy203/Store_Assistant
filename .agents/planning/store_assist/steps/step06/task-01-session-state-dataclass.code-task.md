# Task: SessionState Dataclass

## Description
Define the `SessionState` dataclass in `store_assistant/agent/session.py` that tracks all per-session counters, flags, timestamps, and termination state. This is the single source of truth for session lifecycle management.

## Background
Each Gradio chat session has independent state. The `SessionState` tracks: unique session ID, start time, off-topic counter, passphrase retry counter, stores saved/retrieved counts, and termination status. It is created when a session starts and passed through every `chat()` call.

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See the `SessionState` dataclass definition in Step 6 of the implementation plan section.

## Technical Requirements
1. Create `store_assistant/agent/session.py`
2. Define `SessionState` as a `@dataclass` with fields exactly as specified in the plan:
   - `session_id: str` — UUID4 string
   - `session_start: datetime`
   - `off_topic_count: int = 0`
   - `passphrase_attempts: int = 0`
   - `stores_saved: int = 0`
   - `stores_retrieved: int = 0`
   - `terminated: bool = False`
   - `termination_reason: str = ""`
3. Provide a factory function `new_session() -> SessionState` that creates a fresh session with `uuid4()` id and `datetime.utcnow()` start time
4. No business logic in this file — pure data structure

## Dependencies
- Step 1 scaffold must be complete

## Implementation Approach
1. Import `dataclass` from `dataclasses`, `datetime` from `datetime`, `uuid4` from `uuid`
2. Define the dataclass with default values for all counters/flags
3. Define `new_session()` as a module-level factory function

## Acceptance Criteria

1. **SessionState Can Be Instantiated via new_session()**
   - Given `new_session()` is called
   - When the result is inspected
   - Then `session_id` is a valid UUID string, `session_start` is a `datetime`, all counters are `0`, `terminated` is `False`

2. **SessionState Fields Are Mutable**
   - Given a `SessionState` instance
   - When `state.off_topic_count += 1` is executed
   - Then `state.off_topic_count` equals `1`

3. **Two Sessions Have Different IDs**
   - Given two calls to `new_session()`
   - When comparing `session_id` fields
   - Then they are different strings

## Metadata
- **Complexity**: Low
- **Labels**: session, state, dataclass
- **Required Skills**: Python dataclasses, uuid, datetime
