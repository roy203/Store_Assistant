import pytest


@pytest.fixture()
def mock_executor(mocker):
    return mocker.patch("store_assistant.agent.agent.agent_executor")


def test_chat_returns_response_and_history(mock_executor):
    mock_executor.invoke.return_value = {"output": "Store saved."}
    from store_assistant.agent.agent import chat

    response, history = chat("Save Walmart", [])
    assert response == "Store saved."
    assert history == [
        {"role": "human", "content": "Save Walmart"},
        {"role": "assistant", "content": "Store saved."},
    ]


def test_chat_history_grows_across_turns(mock_executor):
    mock_executor.invoke.return_value = {"output": "Done."}
    from store_assistant.agent.agent import chat

    existing = [
        {"role": "human", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
    ]
    _, new_history = chat("Save Target", existing)
    assert len(new_history) == 4
    assert new_history[2]["content"] == "Save Target"
    assert new_history[3]["content"] == "Done."


def test_chat_invokes_executor_with_input(mock_executor):
    mock_executor.invoke.return_value = {"output": "OK"}
    from store_assistant.agent.agent import chat

    chat("test message", [])
    call_kwargs = mock_executor.invoke.call_args[0][0]
    assert call_kwargs["input"] == "test message"
    assert "history" in call_kwargs


def test_chat_passes_history_as_lc_messages(mock_executor):
    from langchain_core.messages import AIMessage, HumanMessage

    mock_executor.invoke.return_value = {"output": "OK"}
    from store_assistant.agent.agent import chat

    history = [
        {"role": "human", "content": "Hi"},
        {"role": "assistant", "content": "Hello"},
    ]
    chat("next", history)
    lc_history = mock_executor.invoke.call_args[0][0]["history"]
    assert isinstance(lc_history[0], HumanMessage)
    assert isinstance(lc_history[1], AIMessage)
