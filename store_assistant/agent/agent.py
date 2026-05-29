from store_assistant.config import config  # must be first to set LangSmith env vars

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from store_assistant.agent.prompts import FAREWELL_SENTINEL, OFF_TOPIC_SENTINEL, prompt_template
from store_assistant.agent.session import SessionState
from store_assistant.agent.summary import generate_and_save_summary
from store_assistant.agent.tools import retrieve_store, save_store

SESSION_ENDED_MSG = "This session has ended. Please refresh to start a new conversation."

llm = ChatOpenAI(model="gpt-4o-mini", api_key=config.openai_api_key)
tools = [save_store, retrieve_store]

agent = create_tool_calling_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)


def _to_lc_messages(history: list[dict]) -> list:
    messages = []
    for msg in history:
        if msg["role"] == "human":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    return messages


def _update_state(response_text: str, state: SessionState) -> None:
    if FAREWELL_SENTINEL in response_text:
        state.terminated = True
        state.termination_reason = "farewell"
        return

    if OFF_TOPIC_SENTINEL in response_text:
        state.off_topic_count += 1
        if state.off_topic_count >= 3:
            state.terminated = True
            state.termination_reason = "off_topic"
        return

    state.off_topic_count = 0

    if "has been saved" in response_text or "Store '" in response_text and "saved" in response_text:
        state.stores_saved += 1

    if "phone number is" in response_text or "phone number:" in response_text.lower():
        state.stores_retrieved += 1

    if "WRONG_PASSPHRASE" in response_text:
        state.passphrase_attempts += 1
        if state.passphrase_attempts >= 3:
            state.passphrase_attempts = 0
    else:
        state.passphrase_attempts = 0


def _clean_response(response_text: str) -> str:
    return response_text.replace(OFF_TOPIC_SENTINEL, "").replace(FAREWELL_SENTINEL, "").strip()


def chat(
    user_message: str,
    history: list[dict],
    state: SessionState,
) -> tuple[str, list[dict], SessionState]:
    if state.terminated:
        updated_history = history + [
            {"role": "human", "content": user_message},
            {"role": "assistant", "content": SESSION_ENDED_MSG},
        ]
        return SESSION_ENDED_MSG, updated_history, state

    lc_history = _to_lc_messages(history)
    result = agent_executor.invoke({"input": user_message, "history": lc_history})
    response_text = result["output"]

    _update_state(response_text, state)

    if state.terminated:
        summary_text = generate_and_save_summary(history, state)
        response_text = _clean_response(response_text) + f"\n\n**Session Summary:** {summary_text}"
    else:
        response_text = _clean_response(response_text)

    updated_history = history + [
        {"role": "human", "content": user_message},
        {"role": "assistant", "content": response_text},
    ]
    return response_text, updated_history, state
