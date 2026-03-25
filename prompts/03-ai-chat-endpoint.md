# AI Chat Endpoint

**Date:** 2026-03-25
**Task:** Create a /api/chat/ endpoint where the user sends a message and a plan ID and gets back an AI response based on that plan's benefits doc
**Category:** backend

---

## Prompt Used

Create a /api/chat/ endpoint where the user sends a message and a plan ID and gets back an AI response based on that plan's benefits doc

---

## Context & Decisions

- The AI call is handled in a thin `ai_agent/service.py` module to keep the view clean and make the agent logic independently testable.
- The system prompt is defined as a constant in `ai_agent/prompts.py` and parameterized with the plan name and SBC extracted text at call time.
- The endpoint validates that the plan exists and has an SBC document with extracted text before calling the API, returning structured errors otherwise.
- `GROQ_API_KEY` is read from environment — never hardcoded.
- Max context guard: SBC text is truncated to 15,000 characters to stay within token limits.
- **Updated:** Switched from Anthropic Claude to Groq (`llama-3.3-70b-versatile`) for free-tier testing.

---

## Output Summary

Added `groq` to `requirements.txt` (replaced `anthropic`). Created `backend/ai_agent/prompts.py` with the system prompt template and `backend/ai_agent/service.py` with the `get_ai_response()` function using the Groq SDK. Added a `ChatView` POST endpoint in `api/views.py` and registered `/api/chat/` in `api/urls.py`.

---
