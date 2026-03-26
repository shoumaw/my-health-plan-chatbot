# Frontend Modlet Pattern Restructure

**Date:** 2026-03-27
**Task:** Reorganize the Vue 3 frontend source files to follow the modlet pattern — colocate each module's component, composable, test, and story files inside their own named folder.
**Category:** frontend | architecture

---

## Prompt Used

I want the frontend to use modlet pattern, so colocate related files together for example composable/useChat/useChat.test.ts composable/useChat/useChat.ts

---

## Context & Decisions

The modlet pattern keeps each unit of code (component, composable, view) self-contained: all its related files (source, test, stories, types) live in a single named folder. This makes it easy to delete, move, or reason about a feature without hunting across multiple top-level directories.

Applied to:
- `composables/useChat/` → `useChat.ts`, `useChat.test.ts`
- `composables/usePlans/` → `usePlans.ts`, `usePlans.test.ts`
- `views/ChatView/` → `ChatView.vue`, `ChatView.test.ts`
- `views/DashboardView/` → `DashboardView.vue`, `DashboardView.test.ts`
- `components/AppHeader/` → `AppHeader.vue`, `AppHeader.test.ts`
- `components/ChatInterface/` → `ChatInterface.vue`, `ChatInterface.test.ts`, `ChatInterface.stories.ts`, `types.ts`

All import paths updated across the codebase after the moves. `router/index.ts` lazy-load paths updated. `vi.mock()` paths in tests updated to match new locations.

---

## Output Summary

All files moved into modlet folders. All internal imports and `vi.mock()` paths updated. 40/40 tests pass. `vue-tsc --build` reports 0 errors.

---

## Notes

- `vite.config.ts` `defineConfig` import changed from `vite` to `vitest/config` to fix a separate type error where `test:` property was not recognised.
- Storybook `main.ts` had `@storybook/addon-essentials` removed — it is bundled into Storybook 8+ core and does not need to be listed as an addon.
