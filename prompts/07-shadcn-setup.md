# shadcn-vue Setup

**Date:** 2026-03-26
**Task:** Install and configure shadcn-vue component library in the Vue 3 / Vite frontend
**Category:** frontend

---

## Prompt Used

install and configure shadcn-vue

---

## Context & Decisions

- shadcn-vue is set up manually (not via CLI) to avoid interactive prompts and stay compatible with Tailwind v4.
- Core deps installed: `reka-ui` (headless primitives), `class-variance-authority`, `clsx`, `tailwind-merge`, `lucide-vue-next`.
- `src/lib/utils.ts` provides the `cn()` helper used by all shadcn components.
- CSS variables for colors/radius are injected into `main.css` using `@layer base` — the standard shadcn theming approach.
- `components.json` is created so the `npx shadcn-vue add <component>` CLI works going forward.

---

## Output Summary

Installed npm dependencies. Created `src/lib/utils.ts`. Added shadcn CSS variable theme to `main.css`. Created `components.json`.

---
