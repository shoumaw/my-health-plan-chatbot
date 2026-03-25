# DRF Serializers, ViewSets & Router URLs

**Date:** 2026-03-25
**Task:** Create REST API endpoints for all models using Django REST Framework — serializers, viewsets, and URLs registered with a router under /api/v1/
**Category:** backend

---

## Prompt Used

Create REST API endpoints for all of them using Django REST
Framework, I need serializers, viewsets, and URLs registered with
a router under /api/v1/

---

## Context & Decisions

- Each model gets a `ModelSerializer` with explicit `fields` (never `"__all__"`) per project conventions.
- `SBCDocument` gets a separate `SBCDocumentWriteSerializer` to handle file uploads, while the read serializer nests plan info.
- All ViewSets use `IsAuthenticated` permission; views remain thin with business logic to be moved to services later.
- The existing `/api/health/` endpoint is preserved; the router is mounted at `/api/v1/` in `config/urls.py`.

---

## Output Summary

Created `api/serializers.py` with read/write serializers for all four models. Updated `api/views.py` with four `ModelViewSet` classes. Updated `api/urls.py` with a `DefaultRouter` registering all four resources. Updated `config/urls.py` to mount the app at `/api/v1/`.

---
