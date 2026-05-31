# Idea Honing — Store Assistant

Requirements clarification Q&A captured during PDD process.

---

## Q1: LLM Framework

Which LLM framework would you like to use?

Options: LangChain, LlamaIndex, PydanticAI, Strands Agents, Agnos, or another preference?

**A1:** LangChain

---

## Q2: LLM Provider & Model

Which LLM provider and model would you like to use?

Options: OpenAI (e.g. gpt-4o, gpt-4o-mini), Anthropic (e.g. claude-3-5-sonnet), AWS Bedrock, a local model via Ollama, or another?

**A2:** OpenAI `gpt-4o-mini`

---

## Q3: Database / Persistence

Which persistence mechanism would you like for storing stores and conversation summaries?

Options:
- SQLite (lightweight SQL, file-based, no server needed)
- JSON file (simplest, human-readable)
- CSV file
- PostgreSQL / MySQL (full SQL server)
- Other

**A3:** SQLite

---

## Q4: Tracing Method

Which tracing/observability method would you like for LLM calls?

Options:
- **LangSmith** — LangChain's native tracing platform (free tier available, requires API key)
- **LangFuse** — open-source LLM observability (self-hostable or cloud)
- **Arize Phoenix** — open-source, runs fully locally, no API key needed
- **Simple file-based logging** — write LLM call inputs/outputs to a local log file (no external service)

**A4:** LangSmith (will need `LANGCHAIN_API_KEY` added to `.env`)

---

## Q5: Demo UI

What kind of UI would you like for the demo?

Options:
- **CLI** — terminal-based chat loop (simplest, no dependencies)
- **Gradio** — lightweight web UI, minimal setup, runs locally
- **Streamlit** — web UI with easy Python integration, runs locally
- **FastAPI + simple HTML** — REST API with a minimal browser frontend

**A5:** Gradio

---

## Q6: Secret Passphrase

The spec requires a secret passphrase to gate store lookups. How would you like this handled?

Options:
- **Hardcoded in config/env** — a fixed passphrase set in `.env` or a config file (simple, easy to change)
- **Hardcoded in code** — a fixed string in the source (least flexible)
- **User-defined at session start** — the user sets the passphrase at the beginning of each session

**A6:** Hardcoded in `.env` (e.g. `STORE_LOOKUP_PASSPHRASE=...`)

---

## Q7: Off-scope Termination Threshold

The spec says the agent should terminate if the user "repeatedly tries to discuss topics outside the agent's scope." How many off-topic attempts before the agent ends the conversation?

Options:
- **2** — terminate after 2 consecutive off-topic messages
- **3** — terminate after 3 consecutive off-topic messages (recommended balance)
- **5** — more lenient, give the user more chances
- Other number

**A7:** 3 consecutive off-topic messages

---

## Q8: Phone Number Validation

What phone format(s) should be accepted as valid?

Options:
- **US only** — e.g. `(555) 555-5555`, `555-555-5555`, `5555555555`, `+15555555555`
- **International** — any format that passes a general international phone regex
- **Flexible** — accept any string that looks like a phone (10+ digits, any separators)

**A8:** US only — accept `(555) 555-5555`, `555-555-5555`, `5555555555`, `+15555555555`

---

## Q9: Duplicate Store Handling

If a user tries to save a store with a name that already exists in the database, what should happen?

Options:
- **Reject** — inform the user the store already exists, do not overwrite
- **Update** — silently update the phone number for the existing store
- **Ask** — ask the user whether they want to update or keep the existing record

**A9:** Update — silently update the phone number for the existing store

---

## Q10: Store Name Lookup — Case Sensitivity

When a user looks up a store by name, should the search be case-sensitive?

Options:
- **Case-insensitive** — "Walmart", "walmart", "WALMART" all match (recommended)
- **Case-sensitive** — exact match required

**A10:** Case-insensitive — "Walmart", "walmart", "WALMART" all match

---

## Q11: Tests

The spec requires at least two tests. What areas would you like the tests to cover?

Options (pick any combination):
- **Phone validation** — test valid/invalid US phone formats
- **Store save & retrieve** — test the database layer directly
- **Passphrase gating** — test that wrong passphrase blocks lookup, correct one allows it
- **Agent conversation flow** — integration test for a full save → retrieve conversation turn
- **Off-topic termination** — test the 3-strike off-topic termination logic

**A11:** All five areas — phone validation, store save & retrieve, passphrase gating, agent conversation flow, off-topic termination

---

## Q12: Project Structure

How would you like the code organized?

Options:
- **Flat** — all Python files in the root directory (simple, good for small projects)
- **Modular** — separate modules/packages (e.g. `agent/`, `db/`, `ui/`, `tests/`) under a `src/` or project folder
- **No preference** — use whatever makes most sense for the scope

**A12:** Modular — separate packages (`agent/`, `db/`, `ui/`, `tests/`) under a project folder

---

## Q13: Conversation Summary — Trigger & Storage

The spec says to generate and save a conversation summary when the session ends. Should the summary also include metadata like timestamp, number of stores saved/retrieved, and session duration?

Options:
- **Minimal** — just a plain-text narrative summary of what happened in the conversation
- **Rich** — narrative summary + metadata (timestamp, stores saved, stores retrieved, session duration)
- **No preference** — whatever is reasonable

**A13:** Rich — narrative summary + metadata (timestamp, stores saved count, stores retrieved count, session duration)

---

## Q14: Passphrase Wrong — Retry or Abort?

When a user provides the wrong passphrase during a store lookup, what should happen?

Options:
- **Single attempt** — inform the user the passphrase is wrong and drop the lookup request (they can try again by asking)
- **Allow retries** — give the user up to N attempts before dropping the request (e.g. 3 retries)

**A14:** Allow retries — up to 3 passphrase attempts before dropping the lookup request

---

## Requirements Clarification Complete
