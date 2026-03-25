---
name: prompt-logger
description: >
  Automatically saves every AI prompt used during the Vitable Health project to a numbered markdown file
  in the prompts/ folder. Use this skill whenever you are about to generate code, architecture, configs,
  or any AI-assisted output for the project — BEFORE writing the actual response. Triggers include any
  request to build, create, scaffold, generate, write, or design any part of the Django backend, Vue frontend,
  AI agent, data models, API endpoints, components, or project configuration. If the user is asking you to
  produce something for the Vitable Health chatbot project, this skill should always run first.
---

# Prompt Logger Skill

This skill ensures every AI prompt used in the Vitable Health project is logged to a `prompts/` folder
so the CTO can review the full AI usage trail.

## When to use

Any time you are about to produce code or design decisions for this project. Log BEFORE writing the main response.

---

## Step-by-Step Instructions

### 1. Determine the next file number

Read the `prompts/` directory to find existing files and determine the next sequential number.

```bash
ls prompts/ 2>/dev/null | sort | tail -1
```

If the folder doesn't exist or is empty, start at `01`.

### 2. Derive the slug from the task

Convert the user's request into a short kebab-case slug (2–4 words max).

Examples:
- "create Django models" → `django-models`
- "build the chat API endpoint" → `chat-api-endpoint`
- "scaffold Vue 3 project" → `vue-scaffold`
- "write PDF ingestion script" → `pdf-ingestion`
- "design the AI system prompt" → `ai-system-prompt`
- "set up Pinia store" → `pinia-store`
- "create serializers" → `drf-serializers`

### 3. Create the file

File name format: `{NN}-{slug}.md` (e.g., `03-chat-api-endpoint.md`)

Write the file to `prompts/` with this template:

```markdown
# {Title}

**Date:** {YYYY-MM-DD}
**Task:** {One-sentence description of what was asked}
**Category:** {backend | frontend | ai-agent | devops | architecture}

---

## Prompt Used

{The exact prompt / instructions sent to the AI, written clearly as if you'd paste it into ChatGPT or Claude directly}

---

## Context & Decisions

{1–3 sentences explaining why this prompt was written this way — what constraints, patterns, or conventions shaped it}

---

## Output Summary

{Brief description of what this prompt produced — filled in after the response is generated}

---

## Notes

{Any follow-up prompts, iterations, or corrections that were made}
```

### 4. Ensure the prompts/ directory exists

```bash
mkdir -p prompts
```

### 5. Then proceed with the main task

After saving the log file, continue with generating the actual code or content the user requested.

---

## Naming Reference

| Task Area                     | Slug Example              |
|-------------------------------|---------------------------|
| Django project setup          | `django-setup`            |
| Django models                 | `django-models`           |
| Django REST serializers       | `drf-serializers`         |
| Django views / viewsets       | `django-views`            |
| Django URL routing            | `django-urls`             |
| PDF ingestion / parsing       | `pdf-ingestion`           |
| AI agent / system prompt      | `ai-system-prompt`        |
| Chat API endpoint             | `chat-api-endpoint`       |
| Authentication / JWT          | `auth-setup`              |
| Vue 3 project scaffold        | `vue-scaffold`            |
| Vue components                | `vue-components`          |
| Pinia store                   | `pinia-store`             |
| API service layer (Vue)       | `vue-api-service`         |
| Chat UI component             | `chat-ui`                 |
| Plan selector component       | `plan-selector`           |
| Tailwind / styling setup      | `tailwind-setup`          |
| Docker / deployment           | `docker-setup`            |
| Prompt log DB model           | `prompt-log-model`        |

---

## Important Rules

- **Always log before responding.** The log captures intent, not just output.
- **Be honest in the prompt.** Write the prompt as it was actually used — don't clean it up retroactively.
- **One file per distinct task.** If a request covers two separate concerns, split into two files.
- **Never skip logging** because the task "seems small." Even a one-liner endpoint deserves a log entry.