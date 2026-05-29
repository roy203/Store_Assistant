import sqlite3
from datetime import datetime

from store_assistant.config import config

STORES_DDL = """
CREATE TABLE IF NOT EXISTS stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    phone TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

SUMMARIES_DDL = """
CREATE TABLE IF NOT EXISTS conversation_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    summary_text TEXT NOT NULL,
    stores_saved INTEGER DEFAULT 0,
    stores_retrieved INTEGER DEFAULT 0,
    session_start TIMESTAMP NOT NULL,
    session_end TIMESTAMP NOT NULL,
    duration_seconds REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


def init_db(db_path: str = None) -> None:
    db_path = db_path or config.store_db_path
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute(STORES_DDL)
        conn.execute(SUMMARIES_DDL)
        conn.commit()


def upsert_store(name: str, phone: str, db_path: str = None) -> None:
    db_path = db_path or config.store_db_path
    init_db(db_path)
    now = datetime.utcnow().isoformat()
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO stores (name, phone, updated_at) VALUES (?, ?, ?) "
            "ON CONFLICT(name) DO UPDATE SET phone=excluded.phone, updated_at=excluded.updated_at",
            (name, phone, now),
        )
        conn.commit()


def get_store(name: str, db_path: str = None) -> dict | None:
    db_path = db_path or config.store_db_path
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT name, phone FROM stores WHERE LOWER(name) = LOWER(?)",
            (name,),
        ).fetchone()
    return dict(row) if row else None


def save_summary(
    session_id: str,
    summary_text: str,
    stores_saved: int,
    stores_retrieved: int,
    session_start: datetime,
    session_end: datetime,
    db_path: str = None,
) -> None:
    db_path = db_path or config.store_db_path
    init_db(db_path)
    duration_seconds = (session_end - session_start).total_seconds()
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO conversation_summaries "
            "(session_id, summary_text, stores_saved, stores_retrieved, "
            "session_start, session_end, duration_seconds) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                session_id,
                summary_text,
                stores_saved,
                stores_retrieved,
                session_start.isoformat(),
                session_end.isoformat(),
                duration_seconds,
            ),
        )
        conn.commit()
