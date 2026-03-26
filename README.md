# Vitable Health — Benefits Chatbot

A web app where employees can chat with an AI agent to understand their health plan benefits.

**Stack:** Django 5 · Vue 3 · Groq LLM API · PostgreSQL

---

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 14+

---

## Setup

### 1. Clone & install root dependencies

```bash
git clone <repo-url>
cd my-health-plan-chatbot
npm install
```

### 2. Environment variables

**Backend** copy and fill in:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```dotenv
DB_NAME=vitable_health
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

GROQ_API_KEY=gsk_...       # get one at console.groq.com (free tier)
MOCK_USER_EMAIL=dan@company.com
```

**Frontend** — no setup needed. The API URL defaults to `http://localhost:8000/api`. If you need to override it, create `frontend/.env`:

```dotenv
VITE_API_URL=http://localhost:8000/api
```

### 3. Run setup & start

```bash
npm run setup   # runs migrations, seeds plans & employee, extracts SBC text
npm run dev     # starts Django (8000) + Vue (5173) concurrently
```

Open [http://localhost:5173](http://localhost:5173).

---

## Getting a Groq API Key

1. Go to [console.groq.com](https://console.groq.com) and sign up.
2. Navigate to **API Keys** → **Create API Key**.
3. Copy the key into `backend/.env` as `GROQ_API_KEY=gsk_...`.

Groq has a generous free tier no credit card required.

I went for Groq since it has a free tier that we can use to test the app.

## Improvements

Things I would improve with more time:

- **Real authentication** — replace the mock auth middleware with a proper JWT login flow 
- **Multi-plan enrollment** — currently only the Bronze Essential plan has an SBC document attached.
- **Error handling & loading states** — the frontend needs better handling for API errors, network timeouts, and empty states.
- **Tests** — add Django unit tests for the AI service and chat endpoint; expand frontend Vitest coverage beyond the current `ChatInterface` test.
- **Docker Compose** — package the whole stack (Django, Vue, Postgres) into a `docker-compose.yml` so setup is a single command with no local dependencies.
- **TanStack Query** — replace the manual Axios composables with TanStack Query for automatic caching, background refetching, and built-in loading/error states on the dashboard data fetching layer but since we do not have a lot of data here and the chat feature is the main functionality for the application, this was not a priority.
- **Object storage for PDFs** — SBC files are currently stored on the local filesystem (`backend/media/`). In production these should live in S3 or equivalent, with Django storing only the file URL.



