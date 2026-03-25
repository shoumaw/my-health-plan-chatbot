# Employee Dashboard — Plan Cards

**Date:** 2026-03-26
**Task:** Build an employee dashboard page that shows health plans as responsive cards with plan name, description, and a "Chat about this plan" button
**Category:** frontend

---

## Prompt Used

We generated the base components needed Card, Button and Badge. Use them to build an employee dashboard page that shows health plans as cards.
Each card should show the plan name, a short description and a button that says "Chat about this plan"
The layout should be responsive

---

## Context & Decisions

- Plans are fetched from `GET /api/v1/plans/` using the existing axios instance.
- A `usePlans` composable handles fetching and state to keep the view thin.
- The dashboard is a new route at `/` (replacing the placeholder HomeView).
- Responsive grid: 1 col on mobile, 2 on md, 3 on lg.
- Each card uses `Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter` from shadcn, plus `Button`.

---

## Output Summary

Created `src/composables/usePlans.ts`, `src/views/DashboardView.vue`. Updated `src/router/index.ts` to use the dashboard as the home route.

---
