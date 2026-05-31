# Store Assistant

A conversational LLM-based agent that saves and retrieves store information.  
Built with Python · LangChain · GPT-4o-mini · SQLite · Gradio · LangSmith.

---

## Features

- **Save stores** — provide a store name and US phone number; validates format and reprompts on invalid input
- **Look up stores** — retrieve a store's phone number by name, gated behind a passphrase
- **Multi-operation sessions** — save and look up as many stores as you want in one conversation
- **Session termination** — ends gracefully on "I'm done" / "I'm good", or after 3 consecutive off-topic messages
- **Conversation summary** — automatically generates and persists a concise summary to SQLite when the session ends
- **LangSmith tracing** — all LLM calls are traced for inspection in the LangSmith dashboard
- **Gradio UI** — browser-based chat interface running locally

---

## Tech Stack

| Layer | Choice |
|---|---|
| Language | Python 3.10 |
| LLM | OpenAI GPT-4o-mini via LangChain |
| Database | SQLite (stdlib `sqlite3`) |
| UI | Gradio `ChatInterface` |
| Tracing | LangSmith |
| Dependency mgmt | pipenv |
| Testing | pytest + pytest-mock |

---

## Project Structure

```
store_assistant/
├── agent/
│   ├── agent.py        # LangChain agent + chat() + termination logic
│   ├── prompts.py      # System prompt with OFF_TOPIC / FAREWELL sentinels
│   ├── session.py      # SessionState dataclass
│   ├── summary.py      # LLM-generated summary + DB persistence
│   ├── tools.py        # save_store and retrieve_store LangChain tools
│   └── utils.py        # Phone validation and normalization
├── db/
│   └── database.py     # SQLite schema, upsert_store, get_store, save_summary
├── ui/
│   └── app.py          # Gradio ChatInterface
├── tests/              # 50 tests across 7 test files
└── config.py           # Loads .env, validates required keys, sets LangSmith env vars
main.py                 # Entry point — launches Gradio on port 7860
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/roy203/Store_Assistant.git
cd Store_Assistant
```

### 2. Install dependencies

```bash
pip install pipenv      # if not already installed
pipenv install
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```
OPENAI_API_KEY=sk-...
LANGCHAIN_API_KEY=ls__...        # from smith.langchain.com
LANGCHAIN_PROJECT=store-assistant
LANGCHAIN_TRACING_V2=true
STORE_LOOKUP_PASSPHRASE=secret123
STORE_DB_PATH=store_assistant.db
```

### 4. Run the app

```bash
pipenv run python main.py
```

Open **http://localhost:7860** in your browser.

---

## Usage

| Goal | What to say |
|---|---|
| Save a store | `Save Walmart, phone 555-123-4567` |
| Look up a store | `What's the phone for Walmart?` — then provide the passphrase when prompted |
| End the session | `I'm done` or `I'm good` |

**Lookup passphrase:** set via `STORE_LOOKUP_PASSPHRASE` in your `.env`

---

## Running Tests

```bash
pipenv run pytest store_assistant/tests/ -v
```

50 tests covering:
- Config loading and missing-key validation
- SQLite schema, upsert (case-insensitive), summary persistence
- Phone number validation (6 formats) and normalization
- Passphrase gating (correct / wrong / store not found)
- Agent `chat()` history management and LangChain message conversion
- Off-topic 3-strike termination and farewell detection
- Summary generation and DB write on session end

---

## LangSmith Tracing

All LLM calls are automatically traced to your LangSmith project.  
View traces at **https://smith.langchain.com** → project `store-assistant`.

---

## Database Schema

```sql
CREATE TABLE stores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    phone TEXT NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE conversation_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    summary_text TEXT NOT NULL,
    stores_saved INTEGER,
    stores_retrieved INTEGER,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    duration_seconds REAL,
    created_at TIMESTAMP
);
```
