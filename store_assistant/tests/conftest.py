import pytest

from store_assistant.db.database import init_db


@pytest.fixture()
def temp_db(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    yield path


@pytest.fixture()
def mock_llm(mocker):
    mock = mocker.MagicMock()
    mock.invoke.return_value.content = "Mocked LLM response."
    return mock


@pytest.fixture()
def mock_config(monkeypatch):
    monkeypatch.setattr("dotenv.load_dotenv", lambda **kwargs: None)
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("LANGCHAIN_API_KEY", "test-lc-key")
    monkeypatch.setenv("STORE_LOOKUP_PASSPHRASE", "testpass")
    monkeypatch.setenv("LANGCHAIN_PROJECT", "test-project")
    monkeypatch.setenv("LANGCHAIN_TRACING_V2", "true")
    monkeypatch.setenv("STORE_DB_PATH", "test.db")
