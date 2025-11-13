# 🚀 IntellyHub

**IntellyHub** is an enterprise automation platform that blends AI-powered workflows, a dynamic plugin ecosystem, and a cloud-native architecture for scale and reliability.

## ✨ Key Capabilities

- 🤖 **AI-Powered Automation**: Deep integration with OpenAI, LangChain, and custom agents
- 🔌 **Dynamic Plugin System**: Distributed plugins with auto-installation and manifest validation
- 👥 **User & Audit Management**: Fine-grained roles, admin control panel, and full audit trail
- 💰 **Billing & Subscriptions**: Stripe-based plans, add-on pods, and detailed usage tracking
- 🔒 **Security Controls**: Optional Redis rate limiting, encrypted secrets, hardened JWT flows
- 📊 **Analytics & BI**: Business KPIs, CSV/Excel exports, and admin dashboards
- ☸️ **Kubernetes Native**: Flow execution delegated to isolated FSM executor containers
- 🌐 **Modern Stack**: Vue 3 frontend + Flask backend + PostgreSQL database
- 🤖 **FSM Engine**: Python runtime that interprets YAML workflows with states, listeners, and plugins

## 📚 Documentation Map

- [docs/README.md](docs/README.md) — global documentation index
- [docs/quick-start.md](docs/quick-start.md) — bring the stack up in minutes via Docker
- [docs/installation.md](docs/installation.md) — prerequisites, manual setup, and environment variables
- [docs/architecture.md](docs/architecture.md) — end-to-end view of frontend, backend, FSM, and infra
- [intellyhub-be/docs/README.md](intellyhub-be/docs/README.md) — backend entry point (API, DB, dev guide)
- [intellyhub-fe/docs/README.md](intellyhub-fe/docs/README.md) — frontend entry point (Vue Flow editor, composables)
- [ai-automation-fsm-py/docs/README.md](ai-automation-fsm-py/docs/README.md) — FSM engine states, listeners, and tooling
- `intellyhub-be/documentazione/` and `ai-automation-fsm-py/documentazione/` — in-depth whitepapers on security fixes, plugin changes, restart strategies, etc.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Frontend    │    │     Backend     │    │    Database     │
│ Vue 3 + Vite    │◄──►│ Flask + SQLA    │◄──►│ PostgreSQL 15   │
│ Port: 5173      │    │ Port: 5000      │    │ Port: 5432      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌───────────────────────────────┐
                    │ Kubernetes Flow Execution     │
                    │ (isolated FSM executor pods)  │
                    └───────────────────────────────┘
                                 │
                    ┌───────────────────────────────┐
                    │ ai-automation-fsm-py Engine    │
                    │ States • Listeners • Plugins   │
                    └───────────────────────────────┘
```

## 📁 Project Structure

```
IntellyHub/
├── intellyhub-be/              # Flask backend API
│   ├── app/                    # Core application packages
│   │   ├── services/           # Business logic (service layer)
│   │   ├── middleware/         # Custom middleware (metrics, auth helpers)
│   │   ├── schemas/            # Marshmallow schemas
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── auth.py             # JWT auth endpoints
│   │   ├── flows.py            # Flow CRUD/execution APIs
│   │   ├── billing.py          # Stripe integration
│   │   ├── admin.py            # Admin panel APIs
│   │   └── analytics.py        # Business intelligence endpoints
│   ├── migrations/             # Alembic migrations
│   ├── tests/                  # Backend test suite
│   ├── Dockerfile              # Backend container definition
│   └── requirements.txt        # Python dependencies
├── intellyhub-fe/              # Vue 3 + Vite frontend
│   ├── src/                    # Components, pages, composables, layouts
│   ├── tests/                  # Vitest suite
│   ├── Dockerfile              # Frontend container definition
│   └── package.json            # Node dependencies and scripts
├── ai-automation-fsm-py/       # FSM execution engine
│   ├── flow/                   # States, listeners, flow parser
│   ├── diagrammi/              # Sample YAML diagrams
│   ├── documentazione/         # Deep-dive docs (DSL, plugins, restarts)
│   ├── test/                   # pytest suite for the engine
│   ├── main.py                 # Entry point with auto-restart
│   ├── package_manager.py      # Plugin dependency management
│   └── Dockerfile              # Executor container
├── docker-compose.yml          # Local orchestration for API + FE + DB
└── README.md                   # This document
```

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Docker and Compose
docker --version          # >= 20.10
docker compose --version  # >= 2.0
```

### 2. Clone and Configure

```bash
git clone https://github.com/kuduk/IntellyHub.git
cd IntellyHub

cd intellyhub-be
cp .env.example .env   # fill in secrets later
cd ..
```

### 3. Start the Stack

```bash
docker compose up --build          # foreground
# or
docker compose up -d --build       # detached

docker compose ps                  # verify services
```

### 4. Initialize the Database

```bash
docker compose exec api python -m flask db upgrade
docker compose exec api python populate_plans.py
docker compose exec api python setup_admin.py
```

### 5. Access Points

- 🌐 Frontend: http://localhost:5173
- 🔌 Backend API: http://localhost:5000
- 📚 Swagger (dev): http://localhost:5000/docs
- 🗄️ PostgreSQL: localhost:5432 (user `user`, password `pass`)

## 🔧 Advanced Configuration

### Core Environment Variables

```bash
# === CORE ===
SECRET_KEY=replace-with-random
JWT_SECRET_KEY=replace-with-random
DATABASE_URL=postgresql+psycopg2://user:pass@db:5432/intellyhub

# === STRIPE ===
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
STRIPE_PRICE_ID_STANDARD=price_standard_plan_id
STRIPE_PRICE_ID_BUSINESS=price_business_plan_id
STRIPE_PRICE_ID_ENTERPRISE=price_enterprise_plan_id

# === AI SERVICES ===
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_ASSISTANT_ID=asst_your_assistant_id

# === KUBERNETES ===
K8S_NAMESPACE=intellyhub-production
FSM_EXECUTOR_IMAGE=fsm-executor:latest

# === SECURITY ===
BCRYPT_ROUNDS=12
JWT_ACCESS_TOKEN_EXPIRES_HOURS=4
JWT_ADMIN_TOKEN_EXPIRES_HOURS=1
```

### Production Extras

```bash
FLASK_ENV=production
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
REDIS_URL=redis://your-redis-host:6379/0
SENTRY_DSN=https://your-sentry-dsn
```

## 📊 Enterprise Features

### Billing
- Plans: Free, Standard, Business, Scale, Enterprise
- Automated subscriptions via Stripe and webhook inbox
- Add-on pods for bursting workloads
- Invoice tracking plus revenue metrics (MRR, churn, conversion)

### Security
- Password policies and brute-force protection
- Signed JWTs with IP/agent validation hooks
- Centralized audit logging for every admin/user action
- Optional Redis-backed rate limiting per endpoint

### Admin Console
- KPI dashboard with rolling 30-day stats
- User management with bulk actions and plan changes
- Subscription management and billing insights
- Alerting for suspicious events and audit exports

### Plugin System
- GitHub-hosted plugin registry with manifest validation
- Auto-install suggestions based on YAML analysis
- Per-flow plugin configuration and hot reload

### Analytics & BI
- Business metrics (MRR, ARPU, conversion, churn)
- System usage (pods, executions, API volume)
- CSV/Excel exports for external processing
- Real-time dashboards backed by the analytics service

## 🧪 Testing

### Backend
```bash
docker compose exec api bash
python -m pytest
python -m pytest --cov=app --cov-report=html
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/security/
```

### Frontend
```bash
docker compose exec frontend sh
npm test
npm run test:ui
npm run test:coverage
npm run test:watch
```

### FSM Engine
```bash
cd ai-automation-fsm-py
pytest
pytest --cov=flow --cov-report=html
pytest test/test_states/ -v
```

## 🤖 FSM Engine Overview (ai-automation-fsm-py)

- YAML-based DSL for describing complex workflows
- Finite-state architecture with transitions, listeners, and scoped variables
- Built-in states: command, if, loop, switch, llm_agent, telegram-bot, facebook, linkedin, rss_reader, text_to_speech, file, end, etc.
- Event listeners: email, webhook, rss, telegram, directory, mqtt, MCP, A2A
- Auto-restart, lazy loading, and dynamic plugin discovery via `STATE_REGISTRY` and `LISTENER_REGISTRY`
- Plugin management through `package_manager.py` and remote manifests

### Sample Flow

```yaml
name: "RSS News Monitor"
description: "Watch RSS feeds and send Telegram notifications for matching stories"

variables:
  telegram_bot_token: "{TELEGRAM_BOT_TOKEN}"
  telegram_chat_id: "{TELEGRAM_CHAT_ID}"
  keywords: ["AI", "automation", "python"]

listener:
  type: rss
  url: "https://feeds.feedburner.com/oreilly/radar"
  check_interval: 300

start_state: process_article

states:
  process_article:
    state_type: if
    condition: "{event.title} contains any {keywords}"
    true_transition: send_notification
    false_transition: end

  send_notification:
    state_type: telegram-bot
    bot_token: "{telegram_bot_token}"
    chat_id: "{telegram_chat_id}"
    message: |
      🔔 **New Relevant Article**

      **Title**: {event.title}
      **Author**: {event.author}
      **Link**: {event.link}
    transition: end

  end:
    state_type: end
```

## 📚 API Reference

Key endpoints (see `intellyhub-be/docs/api-reference.md` for full details):

- **Auth**: `POST /api/auth/register`, `POST /api/auth/login`, `GET /api/auth/me`
- **Flows**: `GET /api/flows`, `POST /api/flows`, `POST /api/flows/<id>/execute`
- **Billing**: `GET /api/billing/plans`, `GET /api/billing/subscription`, `POST /api/billing/create-checkout-session`
- **Admin**: `GET /api/admin/dashboard`, `GET /api/admin/users`
- **Analytics**: `GET /api/analytics/conversion-rate`, `GET /api/exports/users?format=csv`
- **Health & Metrics**: `GET /health`, `GET /api/metrics`, `GET /api/health?detailed=true`

## 🔍 Monitoring & Observability

```bash
curl http://localhost:5000/api/metrics         # Prometheus metrics
curl http://localhost:5000/api/health?detailed=true
curl -X GET http://localhost:5000/api/system-metrics -H "Authorization: Bearer ADMIN_TOKEN"

docker compose logs -f api
docker compose logs -f frontend
```

## 🛠️ Development Workflow

```bash
# Backend
cd intellyhub-be
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
python setup_admin.py
python run.py

# Frontend
cd intellyhub-fe
npm install
npm run dev
```

- Docker Compose is configured for hot reload (bind mounting code into containers)
- Database migrations via `flask db migrate` / `flask db upgrade`

## 🚢 Deployment

### Docker Swarm (excerpt)
```yaml
version: '3.8'
services:
  api:
    image: intellyhub/backend:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql+psycopg2://user:pass@db:5432/intellyhub
    volumes:
      - flows_data:/data/flows

  frontend:
    image: intellyhub/frontend:latest
    deploy:
      replicas: 2
    ports:
      - "80:80"
```

### Kubernetes (excerpt)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intellyhub-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: intellyhub-api
  template:
    metadata:
      labels:
        app: intellyhub-api
    spec:
      containers:
        - name: api
          image: intellyhub/backend:latest
          ports:
            - containerPort: 5000
          envFrom:
            - configMapRef:
                name: intellyhub-config
```

## 📈 Performance & Scaling

- API response time: < 200 ms (p95)
- Database queries: < 50 ms (p95) with prepared statements and indexes
- Flow execution: < 30 s for standard automations
- Concurrent users: 1000+ supported with horizontal scaling
- Pod capacity: 100+ FSM pods in parallel for enterprise plans

Optimizations: database connection pooling, Redis caching, gzip compression, frontend code splitting, load-balanced deployments, CDN distribution.

## 🤝 Contributing

```bash
gh repo fork kuduk/IntellyHub
git checkout -b feature/my-feature
# make changes
git commit -m "feat: add my feature"
git push origin feature/my-feature
gh pr create --title "Feature: My Feature"
```

Quality bar:
- ✅ Test coverage ≥ 80% backend / ≥ 70% frontend
- ✅ Linting (Pylint/ESLint) passes
- ✅ Security scanning for dependencies
- ✅ Documentation updated alongside code

IntellyHub is in active development—open issues or discussions if you find discrepancies or want to propose improvements.
