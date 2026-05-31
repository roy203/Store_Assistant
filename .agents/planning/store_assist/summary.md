# Project Summary — Store Assistant

## Artifacts Created

```
.agents/planning/store_assist/
├── resources/
│   └── store_assistant.md          # Original take-home spec (reference)
├── rough-idea.md                   # Captured rough idea with env notes
├── idea-honing.md                  # 14-question requirements Q&A
├── design/
│   └── detailed-design.md          # Full design doc with architecture, data models, error handling
├── implementation/
│   └── plan.md                     # 10-step implementation plan with checklist
└── summary.md                      # This document
```

---

## Key Design Decisions

- **LangChain + gpt-4o-mini** — tool-calling agent with `create_tool_calling_agent` + `AgentExecutor`
- **SQLite** — two tables: `stores` (upsert, COLLATE NOCASE) and `conversation_summaries`
- **LangSmith** — automatic tracing via env vars, zero extra code
- **Gradio** — `ChatInterface` wrapping the agent's `chat()` function
- **Modular structure** — `agent/`, `db/`, `ui/`, `tests/` under `store_assistant/`
- **Passphrase** — stored in `.env` as `STORE_LOOKUP_PASSPHRASE`, up to 3 retries per lookup
- **Off-topic termination** — 3-strike counter, resets on in-scope message
- **Rich summary** — LLM-generated narrative + timestamp, duration, stores saved/retrieved count

---

## Design Overview

The agent is a conversational store directory. Users can save stores (name + US phone) and retrieve them (passphrase-gated). The LangChain agent uses two tools (`save_store`, `retrieve_store`) and maintains session state for termination logic. On exit (farewell or 3 off-topic strikes), the LLM generates a summary saved to SQLite.

---

## Implementation Plan Summary

| Step | Focus | Key Output |
|------|-------|------------|
| 1 | Scaffold + config | `Pipfile`, `config.py`, `.env.example`, directory tree |
| 2 | Database layer | `db/database.py`, schema, CRUD, tests |
| 3 | Phone validation | `validate_phone()`, `normalize_phone()`, tests |
| 4 | LangChain tools | `save_store`, `retrieve_store`, passphrase tests |
| 5 | Agent core | `agent.py`, system prompt, tool binding, history |
| 6 | Session state | `SessionState`, off-topic/passphrase/farewell logic |
| 7 | Summary generation | LLM summary + DB persistence on termination |
| 8 | Gradio UI | `ui/app.py`, `main.py`, local web interface |
| 9 | LangSmith tracing | Env var wiring, verified via dashboard |
| 10 | Full test suite | All 5 test files green, end-to-end smoke test |

---

## Environment Setup

```bash
# Required .env keys
OPENAI_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=store-assistant
STORE_LOOKUP_PASSPHRASE=...

# Run
pipenv install
pipenv run python main.py

# Test
pipenv run pytest tests/ -v
```

---

## Next Steps

1. Run `code-task-generator` on this plan to break steps into granular tasks
2. Implement Step 1 first (scaffold + config) — all other steps depend on it
3. Add `LANGCHAIN_API_KEY` and `STORE_LOOKUP_PASSPHRASE` to your `.env` file
4. Implement steps sequentially — each step's tests must pass before moving to the next
