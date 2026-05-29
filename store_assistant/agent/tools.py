from langchain_core.tools import tool

from store_assistant.agent.utils import normalize_phone, validate_phone
from store_assistant.config import config
from store_assistant.db.database import get_store, upsert_store

INVALID_PHONE_MSG = (
    "Invalid phone number. Please provide a US phone number in one of these formats: "
    "(555) 555-5555, 555-555-5555, 5555555555, +15555555555"
)
WRONG_PASSPHRASE_MSG = "WRONG_PASSPHRASE"
STORE_NOT_FOUND_MSG = "STORE_NOT_FOUND"


@tool
def save_store(name: str, phone: str) -> str:
    """Use this tool to save a store's name and phone number to the database.
    Call this when the user wants to add or update a store record.
    Args:
        name: The name of the store (e.g. 'Walmart').
        phone: The US phone number for the store.
    """
    if not validate_phone(phone):
        return INVALID_PHONE_MSG
    normalized = normalize_phone(phone)
    upsert_store(name, normalized)
    return f"Store '{name}' has been saved with phone number {normalized}."


@tool
def retrieve_store(name: str, passphrase: str) -> str:
    """Use this tool to look up a store's phone number from the database.
    A passphrase is required before performing the lookup.
    Call this when the user wants to find a store's phone number and has provided the passphrase.
    Args:
        name: The name of the store to look up.
        passphrase: The secret passphrase provided by the user.
    """
    if passphrase != config.store_lookup_passphrase:
        return WRONG_PASSPHRASE_MSG
    result = get_store(name)
    if result is None:
        return STORE_NOT_FOUND_MSG
    return result["phone"]
