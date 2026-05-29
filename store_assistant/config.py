import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    openai_api_key: str
    langchain_api_key: str
    store_lookup_passphrase: str
    langchain_tracing_v2: str = "true"
    langchain_project: str = "store-assistant"
    store_db_path: str = "store_assistant.db"


def _load_config() -> Config:
    required = {
        "OPENAI_API_KEY": "openai_api_key",
        "LANGCHAIN_API_KEY": "langchain_api_key",
        "STORE_LOOKUP_PASSPHRASE": "store_lookup_passphrase",
    }
    values: dict = {}
    missing = []
    for env_key, field_name in required.items():
        val = os.environ.get(env_key)
        if not val:
            missing.append(env_key)
        else:
            values[field_name] = val

    if missing:
        raise ValueError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Check your .env file against .env.example."
        )

    values["langchain_tracing_v2"] = os.environ.get("LANGCHAIN_TRACING_V2", "true")
    values["langchain_project"] = os.environ.get("LANGCHAIN_PROJECT", "store-assistant")
    values["store_db_path"] = os.environ.get("STORE_DB_PATH", "store_assistant.db")

    cfg = Config(**values)

    os.environ["LANGCHAIN_TRACING_V2"] = cfg.langchain_tracing_v2
    os.environ["LANGCHAIN_API_KEY"] = cfg.langchain_api_key
    os.environ["LANGCHAIN_PROJECT"] = cfg.langchain_project

    return cfg


config = _load_config()
