# Django Models — Employee, Plan, Enrollment, SBCDocument

**Date:** 2026-03-25
**Task:** Create the core Django ORM models for the health benefits chatbot: Employee, Plan, Enrollment, and SBCDocument.
**Category:** backend

---

## Prompt Used

I'm building a Django backend for a health benefits chatbot.
Employees are enrolled in health plans and each plan has a PDF
document (Summary of Benefits).

Let's start by creating the models

Models required:
1. Employee
2. Plan
3. Enrollment (Employees connection to a plan)
4. SBCDocument

---

## Context & Decisions

- `TimeStampedModel` is defined as an abstract base in the same file to keep things self-contained in the single `api` app.
- `Employee` uses a `OneToOneField` to `django.contrib.auth.models.User` rather than a custom user model to stay non-destructive at this early stage.
- `SBCDocument` uses `FileField(upload_to='sbc_documents/')` and also stores `extracted_text` as a TextField so the AI agent can work with pre-parsed content without re-parsing the PDF on every request.

---

## Output Summary

Produced `api/models.py` with `TimeStampedModel`, `Employee`, `Plan`, `Enrollment`, and `SBCDocument`, plus an initial migration.

---
