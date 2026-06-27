# LeadPulse AI

> AI-powered lead qualification, CRM synchronization, and sales intelligence.

## Overview

LeadPulse AI connects Wolfpack lead intake to your Gorilla CRM with an AI qualification layer in the middle — scoring leads, summarizing conversations, and tracking every deal from first contact to closed revenue.

## Tech Stack

| Layer       | Tech                              |
|-------------|-----------------------------------|
| Frontend    | React + TypeScript + Vite         |
| Backend     | FastAPI (Python)                  |
| Database    | PostgreSQL                        |
| ORM         | SQLAlchemy + Alembic              |
| Auth        | JWT (python-jose + passlib)       |
| AI          | Anthropic Claude API              |
| CRM         | Gorilla (modular integration)     |
| Deployment  | Docker + docker-compose           |

## Project Structure

```
leadpulse/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Route handlers
│   │   ├── core/               # Config, security
│   │   ├── db/                 # Session, base class
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── schemas/            # Pydantic request/response schemas
│   │   ├── services/           # Business logic
│   │   └── utils/              # Helpers
│   ├── alembic/                # DB migrations
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/         # React components
│       ├── pages/              # Page-level views
│       ├── hooks/              # Custom React hooks
│       ├── lib/                # API client, utils
│       ├── store/              # State management
│       └── types/              # TypeScript interfaces
└── docker-compose.yml
```

## Database Schema

### Tables

- **users** — Sales reps, managers, admins
- **leads** — Core lead record (contact info, status, AI score, revenue)
- **lead_events** — Immutable audit trail powering the Lead Journey timeline
- **ai_qualifications** — Full AI conversation + structured extraction per lead
- **gorilla_syncs** — CRM push status and payload history

## Quick Start

```bash
# 1. Clone and configure
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 2. Start services
docker-compose up -d

# 3. Run migrations
docker-compose exec backend alembic upgrade head

# 4. Visit
# API docs:  http://localhost:8000/api/docs
# Frontend:  http://localhost:5173
```

## Build Roadmap

- [x] Phase 0 — Project structure & database design
- [ ] Phase 1 — Authentication (login, JWT, roles)
- [ ] Phase 2 — Lead intake + AI qualification
- [ ] Phase 3 — Gorilla CRM integration
- [ ] Phase 4 — Analytics dashboard
- [ ] Phase 5 — AI insights engine
