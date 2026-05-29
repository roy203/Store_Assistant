import pytest

from store_assistant.agent.session import new_session


@pytest.fixture()
def mock_executor(mocker):
    return mocker.patch("store_assistant.agent.agent.agent_executor")


def test_chat_returns_response_and_history(mock_executor):
    mock_executor.invoke.return_value = {"output": "Store saved."}
    from store_assistant.agent.agent import chat

    response, history, state = chat("Save Walmart", [], new_session())
    assert response == "Store saved."
    assert history[0] == {"role": "human", "content": "Save Walmart"}
    assert history[1]["role"] == "assistant"


def test_chat_history_grows_across_turns(mock_executor):
    mock_executor.invoke.return_value = {"output": "Done."}
    from store_assistant.agent.agent import chat

    existing = [
        {"role": "human", "content": "Hello"},
        {"role": "assistant", "content": "Hi!"},
    ]
    _, new_history, _ = chat("Save Target", existing, new_session())
    assert len(new_history) == 4
    assert new_history[2]["content"] == "Save Target"
    assert new_history[3]["content"] == "Done."


def test_chat_invokes_executor_with_input(mock_executor):
    mock_executor.invoke.return_value = {"output": "OK"}
    from store_assistant.agent.agent import chat

    chat("test message", [], new_session())
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
    chat("next", history, new_session())
    lc_history = mock_executor.invoke.call_args[0][0]["history"]
    assert isinstance(lc_history[0], HumanMessage)
    assert isinstance(lc_history[1], AIMessage)


def test_summary_called_on_farewell_termination(mocker, tmp_path):
    from store_assistant.agent.prompts import FAREWELL_SENTINEL

    mock_exec = mocker.patch("store_assistant.agent.agent.agent_executor")
    mock_exec.invoke.return_value = {"output": f"{FAREWELL_SENTINEL} Goodbye!"}

    mock_summary = mocker.patch("store_assistant.agent.agent.generate_and_save_summary")
    mock_summary.return_value = "User saved Walmart and retrieved its phone number."

    from store_assistant.agent.agent import chat

    state = new_session()
    response, _, returned_state = chat("I'm done", [], state)

    assert returned_state.terminated is True
    assert returned_state.termination_reason == "farewell"
    mock_summary.assert_called_once()
    assert "User saved Walmart" in response


def test_summary_saved_to_db_on_termination(mocker, tmp_path):
    import sqlite3

    from store_assistant.agent.prompts import FAREWELL_SENTINEL
    from store_assistant.db.database import init_db

    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    mocker.patch("store_assistant.db.database.config.store_db_path", db_path)
    mocker.patch("store_assistant.agent.summary.config.store_db_path", db_path)

    mock_exec = mocker.patch("store_assistant.agent.agent.agent_executor")
    mock_exec.invoke.return_value = {"output": f"{FAREWELL_SENTINEL} Goodbye!"}

    mock_llm = mocker.patch("store_assistant.agent.summary._summary_llm")
    mock_llm.invoke.return_value.content = "Test summary text."

    from store_assistant.agent.agent import chat

    state = new_session()
    chat("I'm done", [], state)

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT summary_text FROM conversation_summaries WHERE session_id=?",
            (state.session_id,),
        ).fetchone()

    assert row is not None
    assert row[0] == "Test summary text."
