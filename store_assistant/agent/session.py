from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class SessionState:
    session_id: str
    session_start: datetime
    off_topic_count: int = 0
    passphrase_attempts: int = 0
    stores_saved: int = 0
    stores_retrieved: int = 0
    terminated: bool = False
    termination_reason: str = ""


def new_session() -> SessionState:
    return SessionState(
        session_id=str(uuid4()),
        session_start=datetime.utcnow(),
    )
