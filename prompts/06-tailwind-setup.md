# TailwindCSS Setup

**Date:** 2026-03-25
**Task:** Install and configure TailwindCSS in the Vue 3 / Vite frontend
**Category:** frontend

---

## Prompt Used

Install and configure tailwind. For now keep the config minimal, we will incorporate a design system and extend the config later

---

## Context & Decisions

- Tailwind v4 is used, which uses a Vite plugin (`@tailwindcss/vite`) instead of a PostCSS config — this is the recommended approach for Vite projects as of Tailwind v4.
- The `@tailwind` directives are added to `src/assets/main.css` (the existing entry CSS file already imported in `main.ts`).
- No separate `tailwind.config.js` is needed with v4 — configuration is CSS-first.

---

## Output Summary

Installed `tailwindcss` and `@tailwindcss/vite`. Added the Vite plugin to `vite.config.ts`. Added `@import "tailwindcss"` to `src/assets/main.css`.

---
