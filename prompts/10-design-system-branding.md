# Design System & Vitable Health Branding

**Date:** 2026-03-26
**Task:** Create a design system with Tailwind design tokens using Vitable Health brand colors, restyle all views and components to match.
**Category:** frontend

---

## Prompt Used

We do not have a Figma design. Create your own styles and come up with a design system. Add design tokens to the Tailwind config. Use the brand colors of Vitable Health as your reference.

---

## Context & Decisions

- Tailwind v4 uses a CSS-first `@theme` block instead of `tailwind.config.js` — all tokens are defined there
- shadcn-vue tokens are HSL values in `@layer base :root {}` — overriding `--primary: 157 84% 39%` sets brand green across all shadcn components with no per-component changes
- Lucide Vue Next (`lucide-vue-next`) was already installed and used for icons throughout
- Inter font loaded from Google Fonts in `index.html` and referenced via `--font-sans` token
- Old Vite template boilerplate in `main.css` and `base.css` (`@media (min-width: 1024px)` with `body { display: flex }` and `#app { display: grid; grid-template-columns: 1fr 1fr }`) was causing layout to be half-width — removed during debugging

---

## Output Summary

- `src/assets/main.css` — fully rewritten with `@theme` brand token scale, shadcn overrides, shadow CSS vars, unlayered `body`/`#app` resets
- `src/assets/base.css` — stripped to a single comment line
- `index.html` — Inter font from Google Fonts, proper title "Vitable Health — Benefits Portal"
- `src/components/AppHeader.vue` — NEW shared sticky header with brand identity
- `src/views/DashboardView.vue` — complete visual overhaul with hero, tier-colored cards
- `src/views/ChatView.vue` — complete visual overhaul with full-height branded layout
- `src/components/chat/ChatInterface.vue` — complete visual overhaul with AI/user bubbles and typing indicator
- All 11 unit tests remained passing after design changes
