# SBC PDF Fixture Seeding

**Date:** 2026-03-26
**Task:** Add a real SBC PDF to `backend/fixtures/sample-sbc.pdf` and extend the `seed_db` management command to extract its text and attach it to the Bronze Essential plan.
**Category:** backend

---

## Prompt Used

Add one real SBC PDF to the repo under `backend/fixtures/sample-sbc.pdf`, then extend the `seed_db` management command to use pdfplumber to extract its text inline and attach the resulting `SBCDocument` to the Bronze Essential plan.

---

## Context & Decisions

- The CMS publishes an official sample completed SBC PDF, which was downloaded programmatically from their website as a realistic fixture covering a full plan year (01/01/2025–12/31/2025, 5 pages, ~15k chars).
- Extraction is done inline with pdfplumber rather than calling the `extract_sbc_text` management command, to keep the seeder self-contained and avoid subprocess overhead.
- The idempotency check uses `hasattr(plan, "sbc_document") and plan.sbc_document.extracted_text` so re-running `seed_db` never overwrites existing data.
- `FIXTURES_DIR` is resolved relative to `__file__` (3 levels up from the management command to `backend/fixtures/`).

---

## Output Summary

- Downloaded `backend/fixtures/sample-sbc.pdf` (440,883 bytes, CMS Jan 2025 edition)
- Updated `seed_db.py`: added imports (`pdfplumber`, `ContentFile`, `SBCDocument`, `os`), module-level `FIXTURES_DIR` / `SAMPLE_SBC_PATH` constants, `self._seed_sbc_document()` call in `handle()`, and the full `_seed_sbc_document()` method
- Verified: `SBCDocument` created with `file = sbc_documents/bronze-essential-sbc.pdf`, `extracted_text` = 15,294 chars

---

## Notes

- `FIXTURES_DIR` path initially had one too many `..` segments (pointing to project root instead of `backend/`); corrected to 3 levels up.
- The Bronze Essential plan is now the only plan with an SBC document — Silver Select and Gold Premium Care still use the `NO_DOCUMENT_SYSTEM_PROMPT` fallback path.
