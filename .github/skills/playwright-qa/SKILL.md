---
name: playwright-qa
description: >
  QA automation skill for the frontend. Triggers automatically in two cases:
  (1) A new UI component is created or significantly changed — use Playwright MCP to open Storybook
  and visually verify all stories for that component render correctly.
  (2) A new feature or user-facing flow is created — use Playwright MCP to open the app in the browser
  and walk through the full flow end-to-end, taking screenshots and asserting key elements are present.
  ALWAYS run this skill after component or feature work is complete, before marking the task done.
---

# Playwright QA Skill

Automated visual and functional QA for the frontend using the Playwright MCP browser tools.

---

## When to trigger

| Work completed | What to test | Where |
|---|---|---|
| New Vue component created or changed | All Storybook stories for that component | `http://localhost:6006` |
| New feature / page / user flow created | Full happy-path walkthrough | `http://localhost:5173` |

Run this skill **after** the code is written and the dev server is running.

---

## Storybook Component Testing (after creating/changing a component)

### 1. Confirm Storybook is running

Navigate to `http://localhost:6006`. If it returns an error, remind the user to run `npm run storybook` first and stop.

### 2. Find the component's stories

The Storybook sidebar URL pattern is:
```
http://localhost:6006/?path=/story/{component-id}--{story-name}
```

Component ID is derived from the file path, e.g.:
- `src/components/chat/ChatInterface.stories.ts` → `chat-chatinterface`

Navigate to each story in sequence. Known stories for existing components:

| Component | Stories |
|---|---|
| `ChatInterface` | `chat-chatinterface--empty`, `chat-chatinterface--with-conversation`, `chat-chatinterface--loading`, `chat-chatinterface--with-error` |

For new components, discover stories by navigating to `http://localhost:6006` and reading the sidebar snapshot.

### 3. For each story, verify

- Take a screenshot
- Assert the key element described by the story name is visible (e.g., loading spinner for "Loading", error banner for "WithError")
- Check no console errors are thrown: use `mcp_playwright_browser_console_messages`
- Check layout fills its container (no obvious clipping or overflow)

### 4. Report findings

After all stories are checked, summarize:
- ✅ Stories that rendered correctly
- ❌ Stories with visual issues, errors, or missing elements
- Screenshot paths for any failures

---

## Feature / Flow Testing (after creating a new feature)

### 1. Confirm the dev server is running

Navigate to `http://localhost:5173`. If it fails, remind the user to run `npm run dev` and stop.

### 2. Walk the happy path

For each new feature, define the happy path as:
> The minimum sequence of steps a real user would take to successfully complete the feature's core action.

Common flows in this project:

**Dashboard → Chat flow:**
1. Load `http://localhost:5173/` → assert plan cards are visible
2. Click "Chat about this plan" on any card → assert navigation to `/chat/:planId`
3. Assert chat interface renders (message input, send button visible)
4. Type a message and click Send → assert message appears in the chat
5. Assert AI response appears (or loading state shows)

**Chat interaction:**
1. Navigate to `/chat/{planId}?planName=Test+Plan`
2. Type a question in the input
3. Press Enter or click Send
4. Assert user message bubble appears on the right
5. Assert loading indicator appears
6. (If backend is running) Assert AI response bubble appears on the left

### 3. Take screenshots at each major step

Use `mcp_playwright_browser_take_screenshot` after each key action to capture state.

### 4. Check for errors

After completing the flow:
- Run `mcp_playwright_browser_console_messages` to check for JS errors
- Run `mcp_playwright_browser_network_requests` to check for failed API calls (4xx/5xx)

### 5. Verify responsive layout

Resize the viewport to mobile (390×844) and repeat the core interaction:
```
mcp_playwright_browser_resize → width: 390, height: 844
```
Assert no content is clipped or overflowing.

### 6. Report findings

Summarize:
- ✅ Steps that passed
- ❌ Steps that failed (with screenshot path and error detail)
- Any console errors or failed network requests
- Mobile layout issues

---

## General rules

- Always take a screenshot before and after interactions to document state changes
- Never consider a component or feature "done" until this skill has run and passed
- If the backend is not running, skip API-dependent assertions and note it in the report
- If a test fails, fix the issue before declaring the task complete — do not skip or suppress failures
