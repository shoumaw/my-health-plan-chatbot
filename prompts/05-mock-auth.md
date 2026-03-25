# Mock Employee Authentication

**Date:** 2026-03-25
**Task:** Hardcode a specific employee from the database as the current user so the chat endpoint can be tested without login
**Category:** backend

---

## Prompt Used

Instead of JWT authentication, I want to mock a logged in employee for now. Can you hardcode a specific employee from the database as the current user so I can test the chat endpoint without dealing with login?

---

## Context & Decisions

- A `MockEmployeeAuthentication` class is created in `api/authentication.py` — it's a DRF `BaseAuthentication` subclass that reads `MOCK_USER_EMAIL` from the environment and returns the matching `User`.
- It is **only active when `DEBUG=True`** — if `DEBUG` is False the class immediately returns `None`, falling through to real auth. This prevents it from ever working in production.
- The `REST_FRAMEWORK` settings block is added to `settings.py` with `MockEmployeeAuthentication` as the sole default authenticator (dev only pattern — will be replaced with JWT later).
- No code changes to views are needed; `request.user` is populated transparently.

---

## Output Summary

Created `api/authentication.py`. Added `REST_FRAMEWORK` config to `settings.py` pointing to the mock authenticator.

---
