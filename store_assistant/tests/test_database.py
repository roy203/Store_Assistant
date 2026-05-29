import sqlite3
from datetime import datetime, timedelta

import pytest

from store_assistant.db.database import get_store, init_db, save_summary, upsert_store


@pytest.fixture()
def db(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


def test_init_db_creates_tables(db):
    with sqlite3.connect(db) as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    assert "stores" in tables
    assert "conversation_summaries" in tables


def test_init_db_is_idempotent(db):
    init_db(db)
    init_db(db)
    with sqlite3.connect(db) as conn:
        count = conn.execute("SELECT COUNT(*) FROM stores").fetchone()[0]
    assert count == 0


def test_upsert_inserts_new_store(db):
    upsert_store("Walmart", "5551234567", db_path=db)
    result = get_store("Walmart", db_path=db)
    assert result is not None
    assert result["name"] == "Walmart"
    assert result["phone"] == "5551234567"


def test_upsert_updates_existing_store(db):
    upsert_store("Walmart", "5551234567", db_path=db)
    upsert_store("Walmart", "5559876543", db_path=db)
    result = get_store("Walmart", db_path=db)
    assert result["phone"] == "5559876543"
    with sqlite3.connect(db) as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM stores WHERE LOWER(name)='walmart'"
        ).fetchone()[0]
    assert count == 1


def test_get_store_case_insensitive(db):
    upsert_store("Walmart", "5551234567", db_path=db)
    assert get_store("walmart", db_path=db) is not None
    assert get_store("WALMART", db_path=db) is not None
    assert get_store("WaLmArT", db_path=db) is not None


def test_get_store_not_found_returns_none(db):
    assert get_store("Target", db_path=db) is None


def test_save_summary_persists_all_fields(db):
    session_start = datetime(2026, 1, 1, 10, 0, 0)
    session_end = datetime(2026, 1, 1, 10, 5, 30)
    save_summary(
        session_id="test-uuid",
        summary_text="User saved Walmart.",
        stores_saved=2,
        stores_retrieved=1,
        session_start=session_start,
        session_end=session_end,
        db_path=db,
    )
    with sqlite3.connect(db) as conn:
        row = conn.execute(
            "SELECT session_id, summary_text, stores_saved, stores_retrieved, duration_seconds "
            "FROM conversation_summaries WHERE session_id='test-uuid'"
        ).fetchone()
    assert row is not None
    assert row[0] == "test-uuid"
    assert row[1] == "User saved Walmart."
    assert row[2] == 2
    assert row[3] == 1
    assert row[4] == pytest.approx(330.0)
