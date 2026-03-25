# Chat Page & ChatInterface Component

**Date:** 2026-03-26
**Task:** Build a chat page with a chat interface component
**Category:** frontend

---

## Prompt Used

Add a chat page with a chat interface component. Where the user can type a message and see the conversation. It should show the user messages on the right and the AI responses on the left. When the user sends a message it should call POST /api/chat/ with the message and the plan ID and display the response.

The chat interface component should be added as a domain component alongside a unit test and a storybook.

---

## Context & Decisions

- **Component location:** `src/components/chat/ChatInterface.vue` — domain component, purely presentational (props in, `send` event out).
- **Types:** `ChatMessage` extracted to `src/components/chat/types.ts` to avoid re-exporting from `.vue` files (TS limitation).
- **Composable:** `src/composables/useChat.ts` — owns `messages`, `loading`, `error`; calls `POST /api/chat/` via the existing axios instance.
- **View:** `src/views/ChatView.vue` — route-level wrapper reading `planId` from route params and `planName` from query string; includes a back button.
- **Route:** `/chat/:planId` added to Vue Router.
- **Dashboard wired:** "Chat about this plan" button on dashboard cards now navigates to the chat route with `planId` and `planName`.
- **Testing:** Vitest + `@vue/test-utils` + `happy-dom` installed. 11 unit tests written and passing.
- **Storybook:** `@storybook/vue3-vite` installed. 4 stories: Empty, WithConversation, Loading, WithError. Fixed TS errors by using an explicit `ChatInterfaceArgs` type instead of `typeof ChatInterface` (Storybook can't infer props from `<script setup>` generics).

---

## Files Created / Modified

| File | Action |
|---|---|
| `src/components/chat/types.ts` | Created — `ChatMessage` interface |
| `src/components/chat/ChatInterface.vue` | Created — presentational chat UI component |
| `src/components/chat/ChatInterface.test.ts` | Created — 11 Vitest unit tests |
| `src/components/chat/ChatInterface.stories.ts` | Created — 4 Storybook stories |
| `src/composables/useChat.ts` | Created — chat state + API call composable |
| `src/views/ChatView.vue` | Created — route-level chat page |
| `src/router/index.ts` | Modified — added `/chat/:planId` route |
| `src/views/DashboardView.vue` | Modified — wired button to navigate to chat |
| `vite.config.ts` | Modified — added Vitest `test` config block |
| `frontend/package.json` | Modified — added `test`, `test:watch`, `storybook`, `build-storybook` scripts |
| `.storybook/main.ts` | Created — Storybook config pointing to `*.stories.ts` |
| `.storybook/preview.ts` | Created — imports Tailwind CSS into Storybook |
