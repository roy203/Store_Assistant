# Rough Idea: Store Assistant

## Source
Take-Home / Code Challenge — Applied AI Candidate

## Description

Build a small conversational LLM-based agent that saves and retrieves store information. It should validate inputs, gate lookups behind a passphrase, persist data, support multiple operations within one session, and wrap up with a saved summary when the user is done or goes off-scope. Deliver a minimal demo UI, include tracing, and add tests to be discussed during a 30-minute call.

## Conversation Requirements

- Allow the user to save a store (grocery store, etc) in a database by asking for store name and phone.
- Validate the phone format and reprompt on invalid input.
- Store the record and confirm success to the user.
- Allow the user to retrieve a store from the database by name.
- Request a secret passphrase (can be anything you choose); perform the lookup only if the passphrase is correct.
- If the lookup succeeds, communicate the store's phone.
- The user should be able to save and retrieve stores as many times as they want, in any order, within the same conversation.
- Terminate the conversation upon receiving utterances such as "I'm done" or "I'm good," or if the user repeatedly tries to discuss topics outside the agent's scope.
- Generate a concise summary of the conversation.
- Save the summary in the database.

## Other Requirements

- Develop in Python with any opensource tools.
- Use any LLM and provider.
- Use an LLM framework such as LangChain, LlamaIndex, PydanticAI, Agnos, etc.
- Use any database (any form of SQL or a json/csv file is acceptable).
- Use a tracing method for LLM calls that allows inspection of past conversations.
- Implement at least two tests.
- Use any UI to demo the agent (CLI, web UI, or Python script) — locally is fine.

## Environment

- Python 3.10.17 via local pipenv environment in the project root directory.
