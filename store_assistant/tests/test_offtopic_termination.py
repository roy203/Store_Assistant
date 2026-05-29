import pytest

from store_assistant.agent.agent import SESSION_ENDED_MSG, _update_state
from store_assistant.agent.prompts import FAREWELL_SENTINEL, OFF_TOPIC_SENTINEL
from store_assistant.agent.session import SessionState, new_session


def make_state(**kwargs) -> SessionState:
    s = new_session()
    for k, v in kwargs.items():
        setattr(s, k, v)
    return s


def test_first_offtopic_increments_counter():
    state = make_state()
    _update_state(f"{OFF_TOPIC_SENTINEL} Sorry, out of scope.", state)
    assert state.off_topic_count == 1
    assert state.terminated is False


def test_second_offtopic_increments_counter():
    state = make_state(off_topic_count=1)
    _update_state(f"{OFF_TOPIC_SENTINEL} Out of scope again.", state)
    assert state.off_topic_count == 2
    assert state.terminated is False


def test_third_offtopic_terminates_session():
    state = make_state(off_topic_count=2)
    _update_state(f"{OFF_TOPIC_SENTINEL} Still out of scope.", state)
    assert state.off_topic_count == 3
    assert state.terminated is True
    assert state.termination_reason == "off_topic"


def test_inscope_message_resets_counter():
    state = make_state(off_topic_count=2)
    _update_state("Store 'Walmart' has been saved with phone number 5551234567.", state)
    assert state.off_topic_count == 0
    assert state.terminated is False


def test_farewell_terminates_session():
    state = make_state()
    _update_state(f"{FAREWELL_SENTINEL} Thank you! Goodbye.", state)
    assert state.terminated is True
    assert state.termination_reason == "farewell"


def test_terminated_session_short_circuits(mocker):
    mock_executor = mocker.patch("store_assistant.agent.agent.agent_executor")
    from store_assistant.agent.agent import chat

    state = make_state(terminated=True)
    response, _, returned_state = chat("anything", [], state)
    assert response == SESSION_ENDED_MSG
    mock_executor.invoke.assert_not_called()
