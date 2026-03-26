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

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```dotenv
SECRET_KEY=any-random-string
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=vitable_health
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

GROQ_API_KEY=gsk_...       # get one at console.groq.com (free tier)
MOCK_USER_EMAIL=dan@company.com
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


