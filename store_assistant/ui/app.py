import gradio as gr

from store_assistant.agent.agent import chat
from store_assistant.agent.session import SessionState, new_session

_state_component = gr.State(new_session)


def chat_fn(message: str, history: list, state: SessionState) -> tuple[str, SessionState]:
    history_dicts = [{"role": m["role"], "content": m["content"]} for m in history]
    response, _, updated_state = chat(message, history_dicts, state)
    return response, updated_state


demo = gr.ChatInterface(
    fn=chat_fn,
    additional_inputs=[_state_component],
    additional_outputs=[_state_component],
    title="Store Directory Assistant",
    description=(
        "Save and look up store phone numbers. "
        "Ask me to save a store (name + phone) or look one up (passphrase required)."
    ),
    type="messages",
)
