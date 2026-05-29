from store_assistant.config import config  # must be first to set LangSmith env vars

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from store_assistant.agent.prompts import prompt_template
from store_assistant.agent.tools import retrieve_store, save_store

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


def chat(user_message: str, history: list[dict]) -> tuple[str, list[dict]]:
    lc_history = _to_lc_messages(history)
    result = agent_executor.invoke({"input": user_message, "history": lc_history})
    response_text = result["output"]
    updated_history = history + [
        {"role": "human", "content": user_message},
        {"role": "assistant", "content": response_text},
    ]
    return response_text, updated_history
