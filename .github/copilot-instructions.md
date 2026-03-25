# Vitable Health — Copilot Instructions

This file defines the coding conventions, architecture decisions, and best practices for the
Vitable Health benefits chatbot project. Follow these guidelines in all code suggestions.

---

## Project Overview

A fullstack web app where employees enrolled in health plans can chat with an AI agent to
understand their plan benefits. Built with **Django (backend)** and **Vue 3 (frontend)**.

---

## Stack

| Layer        | Technology                                      |
|--------------|-------------------------------------------------|
| Frontend     | Vue 3, Vite, Pinia, Vue Router, TailwindCSS     |
| Backend      | Django 5, Django REST Framework                 |
| Database     | SQLite (dev) / PostgreSQL (prod-ready)          |
| AI           | Anthropic Claude API (via `anthropic` SDK)      |
| PDF Parsing  | `pdfplumber`                                    |
| Auth         | JWT via `djangorestframework-simplejwt`         |

---

## Repository Structure

```
vitable-health/
├── backend/                   # Django project
│   ├── config/                # settings, urls, wsgi
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── dev.py
│   │   │   └── prod.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── accounts/          # Employee auth & profiles
│   │   ├── plans/             # Plan, Enrollment, SBF models
│   │   ├── chat/              # Chat session & message models
│   │   └── ai_agent/          # AI logic, prompt building, PDF ingestion
│   ├── manage.py
│   └── requirements.txt
├── frontend/                  # Vue 3 project (Vite)
│   ├── src/
│   │   ├── assets/
│   │   ├── components/        # Reusable UI components
│   │   ├── views/             # Route-level page components
│   │   ├── stores/            # Pinia stores
│   │   ├── services/          # API call functions
│   │   ├── composables/       # Reusable Vue composition functions
│   │   ├── router/
│   │   └── main.js
│   ├── index.html
│   └── vite.config.js
├── prompts/                   # AI prompt logs (dev tool for CTO review)
│   └── NN-slug.md
└── .github/
    └── copilot-instructions.md
```

---

## Django Conventions

### Models

- All models inherit from a `TimeStampedModel` base with `created_at` and `updated_at`
- Use `UUIDField` as primary key on all models: `id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`
- Use `snake_case` for all field names
- Always define `__str__`, `class Meta`, and `verbose_name`

```python
# Good
class Plan(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"
        ordering = ["name"]

    def __str__(self):
        return self.name
```

### Serializers

- Use `ModelSerializer` for all model-based serializers
- Always explicitly declare `fields` — never use `fields = "__all__"`
- Nested serializers should be read-only by default; use separate write serializers for mutations
- Name pattern: `{Model}Serializer`, `{Model}WriteSerializer`

### Views & ViewSets

- Use `ViewSet` / `ModelViewSet` from DRF for all CRUD resources
- Keep views thin — business logic lives in `services.py` or `ai_agent/`
- All views require authentication unless explicitly marked `permission_classes = [AllowAny]`
- Use `@action` decorator for non-standard endpoints

```python
# Good — thin view, logic in service
class ChatViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        response = chat_service.send_message(
            user=request.user,
            message=request.data.get("message"),
            plan_id=request.data.get("plan_id"),
        )
        return Response(response)
```

### URL Patterns

- All API routes prefixed with `/api/v1/`
- Use DRF `DefaultRouter` for ViewSets
- Name routes using the format `{resource}-{action}` (auto-handled by router)

### Settings

- Never hardcode secrets — use `python-decouple` or `os.environ`
- Split settings into `base.py`, `dev.py`, `prod.py`
- `DEBUG = True` only in `dev.py`

### Error Handling

- Return structured error responses: `{"error": "message", "code": "ERROR_CODE"}`
- Use DRF exception handlers — don't return raw 500s
- Log exceptions with `logger = logging.getLogger(__name__)`

---

## Vue 3 Conventions

### Component Style

- Use **Composition API** with `<script setup>` syntax exclusively — no Options API
- One component per file
- Component file names: `PascalCase.vue` (e.g., `ChatWindow.vue`, `PlanCard.vue`)
- Template-only presentational components: prefix with `Base` (e.g., `BaseButton.vue`)

```vue
<!-- Good -->
<script setup>
import { ref, computed } from 'vue'
import { useChatStore } from '@/stores/chat'

const props = defineProps({
  planId: { type: String, required: true }
})

const store = useChatStore()
const message = ref('')

const sendMessage = async () => {
  await store.sendMessage(props.planId, message.value)
  message.value = ''
}
</script>
```

### State Management (Pinia)

- One store per domain: `useAuthStore`, `useChatStore`, `usePlanStore`
- Store file names: `camelCase.js` inside `stores/`
- Actions are `async` by default if they touch the API
- Never mutate state directly outside of store actions

### API Services

- All API calls live in `src/services/` — never inline fetch/axios in components
- One file per resource: `auth.service.js`, `plans.service.js`, `chat.service.js`
- Use `axios` with a configured base instance in `services/api.js`
- Attach JWT token via axios interceptor — not per-request

```js
// services/api.js
import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL })

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default api
```

### Composables

- Extract reusable reactive logic into `composables/use{Name}.js`
- Examples: `useChat.js`, `usePlan.js`, `useAuth.js`

### Routing

- Route names in `camelCase`: `chatView`, `planList`, `login`
- Lazy-load all route components: `component: () => import('@/views/ChatView.vue')`
- Use navigation guards for auth protection at the router level

### Environment Variables

- All env vars prefixed with `VITE_` for frontend
- Never commit `.env` files — always provide `.env.example`

---

## AI Agent Conventions

### System Prompt Design

- System prompts live in `backend/apps/ai_agent/prompts.py` as Python constants
- Prompts are parameterized with f-strings or `.format()` — never concatenated ad hoc
- Every system prompt has a corresponding entry in the `prompts/` log folder

### Context Injection

- SBF document content is injected per-request based on the employee's enrolled plan
- Context is truncated to stay within token limits — use character count guards
- Never send raw PDF binary — always extract and clean text first

### Prompt Logging (Runtime)

- Every AI call is logged to the `PromptLog` model with: `employee`, `plan`, `user_message`, `system_prompt`, `ai_response`, `created_at`
- Logging is non-blocking — failures to log should not break the chat flow

---

## General Conventions

### Git

- Branch naming: `feature/`, `fix/`, `chore/` prefixes (e.g., `feature/chat-endpoint`)
- Commit messages: imperative mood, present tense (`Add chat serializer`, not `Added...`)
- Never commit: `.env`, `__pycache__`, `node_modules`, `*.pyc`, `db.sqlite3`, media files

### Naming

| Thing             | Convention      | Example                    |
|-------------------|-----------------|----------------------------|
| Python files      | `snake_case`    | `chat_service.py`          |
| Python classes    | `PascalCase`    | `ChatSession`              |
| Python functions  | `snake_case`    | `build_system_prompt()`    |
| Vue components    | `PascalCase`    | `ChatWindow.vue`           |
| Vue composables   | `camelCase`     | `useChat.js`               |
| Pinia stores      | `camelCase`     | `useChatStore.js`          |
| CSS classes       | Tailwind only   | `flex gap-4 text-sm`       |
| API routes        | `kebab-case`    | `/api/v1/chat-sessions/`   |
| DB columns        | `snake_case`    | `created_at`, `plan_name`  |

### Code Quality

- Backend: `black` for formatting, `flake8` for linting
- Frontend: `eslint` + `prettier`
- No `console.log` in committed code (use `logger` on backend, remove on frontend)
- All functions and components should do one thing well

---

## Prompt Log Convention (Dev AI Trail)

Every AI-assisted task during development should produce a file in `prompts/`:

```
prompts/
  01-django-models.md
  02-drf-serializers.md
  03-pdf-ingestion.md
  04-ai-system-prompt.md
  05-chat-api-endpoint.md
  06-vue-scaffold.md
  ...
```

Each file documents: the prompt used, why it was written that way, and what it produced.
This is a first-class project artifact — treat it like documentation.