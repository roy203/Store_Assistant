import pytest

from store_assistant.agent.tools import STORE_NOT_FOUND_MSG, WRONG_PASSPHRASE_MSG
from store_assistant.db.database import init_db, upsert_store


@pytest.fixture()
def db(tmp_path, monkeypatch):
    path = str(tmp_path / "test.db")
    init_db(path)
    monkeypatch.setattr("store_assistant.db.database.config.store_db_path", path)
    monkeypatch.setattr("store_assistant.agent.tools.config.store_lookup_passphrase", "testpass")
    upsert_store("Walmart", "5551234567", db_path=path)
    return path


def test_correct_passphrase_returns_phone(db):
    from store_assistant.agent.tools import retrieve_store
    result = retrieve_store.invoke({"name": "Walmart", "passphrase": "testpass"})
    assert result == "5551234567"


def test_wrong_passphrase_returns_sentinel(db):
    from store_assistant.agent.tools import retrieve_store
    result = retrieve_store.invoke({"name": "Walmart", "passphrase": "wrongpass"})
    assert result == WRONG_PASSPHRASE_MSG


def test_correct_passphrase_store_not_found(db):
    from store_assistant.agent.tools import retrieve_store
    result = retrieve_store.invoke({"name": "Target", "passphrase": "testpass"})
    assert result == STORE_NOT_FOUND_MSG


def test_lookup_is_case_insensitive(db):
    from store_assistant.agent.tools import retrieve_store
    result = retrieve_store.invoke({"name": "walmart", "passphrase": "testpass"})
    assert result == "5551234567"


def test_save_store_valid_phone(db):
    from store_assistant.agent.tools import save_store
    result = save_store.invoke({"name": "Target", "phone": "555-987-6543"})
    assert "Target" in result
    assert "saved" in result.lower()


def test_save_store_invalid_phone(db):
    from store_assistant.agent.tools import save_store
    result = save_store.invoke({"name": "Target", "phone": "123"})
    assert "Invalid phone" in result
