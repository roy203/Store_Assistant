# Task: Gradio Chat UI

## Description
Implement `store_assistant/ui/app.py` with a Gradio `ChatInterface` that wires to the agent's `chat()` function with per-session state management, and update `main.py` to launch the interface.

## Background
Gradio's `ChatInterface` provides a ready-made chat UI. The `fn` parameter receives `(message, history)` from Gradio and must return the response string. Session state (`SessionState`) must be maintained per session using `gr.State`. After termination, further messages should receive a friendly "session ended" reply (which the agent already handles via the guard in `chat()`).

## Reference Documentation
**Required:**
- Design: `.agents/planning/store_assist/design/detailed-design.md`

**Note:** You MUST read the detailed design document before beginning implementation. See Step 8 and the "ui/app.py" section under Components and Interfaces.

## Technical Requirements
1. Create `store_assistant/ui/app.py`
2. Use `gr.ChatInterface` with a wrapper function that adapts Gradio's `(message, history)` to `agent.chat(message, history, state)`
3. Manage `SessionState` via `gr.State(new_session)` so each browser session gets its own state
4. The Gradio wrapper function signature: `def chat_fn(message: str, history: list, state: SessionState) -> tuple[str, SessionState]`
5. Set `title="Store Assistant"` and `description` on the interface
6. Export a `demo` variable (the `gr.ChatInterface` or `gr.Blocks` instance) for `main.py` to call `.launch()`
7. Update `main.py`: `from store_assistant.ui.app import demo; demo.launch()`
8. Interface must launch on `http://localhost:7860`

## Dependencies
- Steps 5–7 (full agent with state and summary) must be complete

## Implementation Approach
1. Import `gradio as gr`, `agent.chat` from `agent.agent`, `new_session` from `agent.session`
2. Define `chat_fn(message, history, state)` that calls `agent.chat()` and returns `(response, updated_state)`
3. Create `demo = gr.ChatInterface(fn=chat_fn, additional_inputs=[gr.State(new_session)], title="Store Assistant", description="...")`
4. In `main.py`: `demo.launch(server_name="0.0.0.0", server_port=7860)`
5. Manual smoke test: launch the app and run a full save → retrieve → "I'm done" conversation

## Acceptance Criteria

1. **App Launches Without Errors**
   - Given valid `.env` with all required keys
   - When `python main.py` is run
   - Then Gradio starts and prints a URL to `http://localhost:7860` with no import or startup errors

2. **chat_fn Accepts Gradio Signature**
   - Given `chat_fn` function in `ui/app.py`
   - When inspecting its signature
   - Then it accepts `(message: str, history: list, state: SessionState)` and returns a string

3. **Session State Is Isolated Per Session**
   - Given two browser tabs opened simultaneously
   - When each runs an independent conversation
   - Then each has its own independent `SessionState` (separate off-topic counters, etc.)

4. **demo Variable Is Exported**
   - Given `from store_assistant.ui.app import demo`
   - When this import is executed
   - Then `demo` is a Gradio `ChatInterface` instance with `launch` method

5. **Existing Tests Still Pass**
   - Given `ui/app.py` and updated `main.py` are added
   - When `pytest tests/ -v` is run
   - Then all previously passing tests continue to pass

## Metadata
- **Complexity**: Low
- **Labels**: gradio, ui, frontend, chat-interface
- **Required Skills**: Gradio, Python, gr.State
