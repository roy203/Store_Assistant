from datetime import datetime

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from store_assistant.agent.session import SessionState
from store_assistant.config import config
from store_assistant.db.database import save_summary

_summary_llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.openai_api_key)


def generate_and_save_summary(history: list[dict], state: SessionState) -> str:
    session_end = datetime.utcnow()

    conversation = "\n".join(
        f"{msg['role'].upper()}: {msg['content']}" for msg in history
    )

    prompt = (
        f"Below is a conversation between a user and a Store Directory Assistant.\n\n"
        f"{conversation}\n\n"
        f"Session stats: stores saved={state.stores_saved}, stores retrieved={state.stores_retrieved}.\n\n"
        f"Write a concise 2-3 sentence summary of what happened in this conversation."
    )

    response = _summary_llm.invoke([HumanMessage(content=prompt)])
    summary_text = response.content

    save_summary(
        session_id=state.session_id,
        summary_text=summary_text,
        stores_saved=state.stores_saved,
        stores_retrieved=state.stores_retrieved,
        session_start=state.session_start,
        session_end=session_end,
    )

    return summary_text
