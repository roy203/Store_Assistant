import importlib
import os

import pytest


def _reload_config(monkeypatch, env_overrides: dict):
    """Reload store_assistant.config with a patched environment."""
    monkeypatch.setattr("dotenv.load_dotenv", lambda **kwargs: None)
    for key, value in env_overrides.items():
        if value is None:
            monkeypatch.delenv(key, raising=False)
        else:
            monkeypatch.setenv(key, value)
    import store_assistant.config as cfg_module
    importlib.reload(cfg_module)
    return cfg_module


FULL_ENV = {
    "OPENAI_API_KEY": "test-openai-key",
    "LANGCHAIN_API_KEY": "test-lc-key",
    "STORE_LOOKUP_PASSPHRASE": "testpass",
    "LANGCHAIN_PROJECT": "test-project",
    "LANGCHAIN_TRACING_V2": "true",
    "STORE_DB_PATH": "test.db",
}


def test_all_keys_loaded(monkeypatch):
    mod = _reload_config(monkeypatch, FULL_ENV)
    assert mod.config.openai_api_key == "test-openai-key"
    assert mod.config.langchain_api_key == "test-lc-key"
    assert mod.config.store_lookup_passphrase == "testpass"
    assert mod.config.langchain_project == "test-project"
    assert mod.config.store_db_path == "test.db"


def test_missing_openai_key_raises(monkeypatch):
    env = {**FULL_ENV, "OPENAI_API_KEY": None}
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        _reload_config(monkeypatch, env)


def test_missing_langchain_api_key_raises(monkeypatch):
    env = {**FULL_ENV, "LANGCHAIN_API_KEY": None}
    with pytest.raises(ValueError, match="LANGCHAIN_API_KEY"):
        _reload_config(monkeypatch, env)


def test_missing_passphrase_raises(monkeypatch):
    env = {**FULL_ENV, "STORE_LOOKUP_PASSPHRASE": None}
    with pytest.raises(ValueError, match="STORE_LOOKUP_PASSPHRASE"):
        _reload_config(monkeypatch, env)


def test_optional_keys_use_defaults(monkeypatch):
    env = {
        "OPENAI_API_KEY": "test-openai-key",
        "LANGCHAIN_API_KEY": "test-lc-key",
        "STORE_LOOKUP_PASSPHRASE": "testpass",
        "LANGCHAIN_PROJECT": None,
        "LANGCHAIN_TRACING_V2": None,
        "STORE_DB_PATH": None,
    }
    mod = _reload_config(monkeypatch, env)
    assert mod.config.store_db_path == "store_assistant.db"
    assert mod.config.langchain_project == "store-assistant"
    assert mod.config.langchain_tracing_v2 == "true"


def test_langsmith_env_vars_set(monkeypatch):
    mod = _reload_config(monkeypatch, FULL_ENV)
    assert os.environ.get("LANGCHAIN_TRACING_V2") == "true"
    assert os.environ.get("LANGCHAIN_API_KEY") == "test-lc-key"
    assert os.environ.get("LANGCHAIN_PROJECT") == "test-project"
