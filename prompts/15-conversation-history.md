# Conversation History

**Date:** 2026-03-29
**Task:** Pass the full accumulated message history to the AI on every request so the model can hold a real multi-turn conversation.
**Category:** ai-agent

---

## Prompt

> Send back the full history with every message as context but pass it through a new `history` parameter which contains the accumulated messages array minus the new message being typed.

---

## Why

The AI service was stateless — each call only sent the latest user message with no prior context. The model couldn't reference anything said earlier in the conversation, making sustained Q&A impossible.

---

## Approach

The frontend (`useChat.ts`) already stores every message in a reactive `messages` array. Before each API call, the array is sliced to exclude the just-added user message, mapped to `{ role, content }` pairs, and sent as a `history` field in the POST body. `views.py` was already reading that field and passing it through to the service. The only missing link was `service.py`, which didn't accept a `history` parameter and didn't include prior turns in the Groq messages array.

**Fix:** Add a `history` parameter to `get_ai_response`, sanitise each entry (accept only `user`/`assistant` roles with string content, drop anything else), then insert the cleaned history turns between the system prompt and the new user message:

```
[system_prompt, ...history_turns, new_user_message]
```

This gives the model full context for every response without any changes needed on the frontend or in views.

---

## What it produced

- Updated `backend/ai_agent/service.py`: `get_ai_response` now accepts `history: list[dict]` and builds a multi-turn messages array.
