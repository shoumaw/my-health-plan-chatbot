# Backend App Restructure

**Date:** 2026-03-26
**Task:** Refactor the Django backend from a single `api/` app into separate domain-scoped apps: `apps/accounts/`, `apps/plans/`, `apps/chat/`
**Category:** backend | architecture

---

## Prompt Used

Refactor the Django backend from a single `api/` app into a separate domain structure

---

## Context & Decisions

Structured this way to match the domain-driven design called out in copilot-instructions.md. `TimeStampedModel` is defined in `accounts/models.py` (the base app) and imported by `plans` — this creates a natural dependency chain (chat → plans → accounts → Django auth) that mirrors real domain ownership. Management commands for data setup and PDF extraction live in `plans` since they operate on plan/SBC data.

---

## Output Summary

Created `apps/` package with three Django apps (`accounts`, `plans`, `chat`). Moved all models, serializers, views, URLs, and management commands to the appropriate app. Updated `config/settings.py` INSTALLED_APPS and REST_FRAMEWORK auth path. Updated `config/urls.py` to include each app's URL module. Generated migrations via `makemigrations`.

