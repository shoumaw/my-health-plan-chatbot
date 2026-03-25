# PDF Ingestion Management Command

**Date:** 2026-03-25
**Task:** Write a Django management command that uses pdfplumber to extract all the text from the PDF and store it in the extracted_text field on SBCDocument
**Category:** backend

---

## Prompt Used

write a Django management command that uses pdfplumber to extract all the text from the PDF and store it in a text field on the model SBCDocument

---

## Context & Decisions

- The command lives at `api/management/commands/extract_sbc_text.py` so it's invokable via `python manage.py extract_sbc_text`.
- It accepts an optional `--plan-id` argument to process a single document; without it, it processes all `SBCDocument` records that have a file but empty `extracted_text`.
- `pdfplumber` opens the file via `document.file.open()` (works with both local FileSystem and cloud storage backends) and joins page text with newlines.
- A `--force` flag re-extracts even if `extracted_text` is already populated.
- `MEDIA_ROOT` and `MEDIA_URL` are added to `settings.py` since they were missing.

---

## Output Summary

Added `pdfplumber` to `requirements.txt`. Added `MEDIA_ROOT`/`MEDIA_URL` to `config/settings.py`. Created `api/management/__init__.py`, `api/management/commands/__init__.py`, and `api/management/commands/extract_sbc_text.py`.

---
