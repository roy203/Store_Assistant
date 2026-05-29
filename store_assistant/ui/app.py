import gradio as gr

from store_assistant.agent.agent import chat
from store_assistant.agent.session import SessionState, new_session


def chat_fn(message: str, history: list, state: SessionState) -> tuple[str, SessionState]:
    response, _, updated_state = chat(message, history, state)
    return response, updated_state


demo = gr.ChatInterface(
    fn=chat_fn,
    additional_inputs=[gr.State(new_session)],
    title="Store Directory Assistant",
    description=(
        "Save and look up store phone numbers. "
        "Ask me to save a store (name + phone) or look one up (passphrase required)."
    ),
    type="messages",
)
