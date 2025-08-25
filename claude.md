# IntellyHub - AI Workflow Orchestration Platform

## 🎯 Panoramica del Progetto

IntellyHub è una piattaforma di orchestrazione AI che permette di creare, gestire ed eseguire workflow complessi e agenti autonomi attraverso un'interfaccia ibrida visual/code. La piattaforma combina la semplicità di strumenti low-code con la potenza di framework AI avanzati.

### Tagline
**"Automations that think"** - Automazioni che pensano

## 🏗️ Architettura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │     Worker      │
│ (Vue 3 + Vutefy)│◄──►│   (Flask)       │◄──►│   (Python)      │
│                 │    │                 │    │                 │
│ • Visual IDE    │    │ • REST API      │    │ • FSM Engine    │
│ • YAML Editor   │    │ • User Mgmt     │    │ • Plugin System │
│ • Flow Designer │    │ • K8s Mgmt      │    │ • AI Integration│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Kubernetes    │
                    │                 │
                    │ • Pod Isolation │
                    │ • Auto Scaling  │
                    │ • Security      │
                    └─────────────────┘
```

## 📁 Struttura del Progetto

```
IntellyHub/
├── intellyhub-be/              # Backend API (Flask)
│   ├── app/                    # Applicazione principale
│   │   ├── services/           # Business logic layer
│   │   ├── models/             # Database models
│   │   ├── routes/             # API endpoints
│   │   └── middleware/         # Custom middleware
│   ├── docker-compose.yml      # Setup Docker attuale
│   ├── Dockerfile
│   └── requirements.txt
│
├── intellyhub-fe/              # Frontend (Vue 3 + TypeScript)
│   ├── src/
│   │   ├── components/         # Componenti Vue
│   │   ├── pages/              # Pagine dell'app
│   │   ├── composables/        # Logic riutilizzabile
│   │   └── locales/            # Internazionalizzazione
│   ├── package.json
│   └── vite.config.ts
│
├── ai-automation-fsm-py/       # Worker Engine
│   ├── main.py                 # Entry point
│   ├── flow/                   # Core engine
│   │   ├── flow.py             # FlowDiagram class
│   │   ├── states/             # Stati disponibili
│   │   ├── listeners/          # Event listeners
│   │   └── plugin_loader.py    # Sistema plugin
│   ├── diagrammi/              # Esempi YAML
│   ├── documentazione/         # Docs tecniche
│   └── requirements.txt
│
└── businessplan/               # Business Plan (LaTeX)
    └── businessplan.tex
```

## 🚀 Setup e Avvio Rapido

### Prerequisiti
- Docker & Docker Compose
- Git
- Node.js 18+ (per sviluppo frontend)
- Python 3.9+ (per sviluppo worker)

### 1. Clone del Progetto
```bash
# Se usi repository separate
git clone <intellyhub-be-repo>
git clone <intellyhub-fe-repo>
git clone <ai-automation-fsm-py-repo>
git clone <businessplan-repo>
```

### 2. Setup Backend + Database
```bash
cd intellyhub-be

# Copia configurazione
cp .env.example .env

# Avvia backend + database
docker-compose up -d

# Verifica
curl http://localhost:5000/api/health
```

### 3. Setup Frontend (Sviluppo)
```bash
cd intellyhub-fe

# Installa dipendenze
npm install

# Avvia dev server
npm run dev

# Apri http://localhost:5713
```

### 4. Setup Worker Engine
```bash
cd ai-automation-fsm-py

# Installa dipendenze
pip install -r requirements.txt

# Copia configurazione
cp .env.example .env

# Test con esempio
python main.py diagrammi/test_telegram_real.yaml
```

## 🔧 Componenti Principali

### Backend (intellyhub-be)
**Stack:** Flask + SQLAlchemy + PostgreSQL + Kubernetes Client

**Funzionalità:**
- API REST per gestione utenti e workflow
- Sistema di autenticazione JWT
- Orchestrazione Kubernetes per esecuzione workflow
- Sistema di plugin dinamico
- Billing e subscription management
- Audit logging avanzato

**Endpoints Principali:**
- `/api/auth/*` - Autenticazione
- `/api/flows/*` - Gestione workflow
- `/api/plugins/*` - Sistema plugin
- `/api/billing/*` - Gestione abbonamenti

### Frontend (intellyhub-fe)
**Stack:** Vue 3 + TypeScript + Vuetify + Vue Flow

**Funzionalità:**
- Editor visuale drag-and-drop per workflow
- Editor YAML sincronizzato
- Dashboard per monitoraggio esecuzioni
- Gestione plugin e marketplace
- Interfaccia multilingue (i18n)

**Componenti Chiave:**
- `FlowDesigner` - Editor visuale
- `YamlEditor` - Editor codice
- `PluginManager` - Gestione plugin
- `Dashboard` - Monitoring

### Worker Engine (ai-automation-fsm-py)
**Stack:** Python + LangChain + Kubernetes

**Funzionalità:**
- Esecuzione workflow in container isolati
- Sistema FSM (Finite State Machine)
- Plugin system estendibile
- Integrazione AI/LLM
- Event listeners (Telegram, Email, RSS, etc.)

**Stati Disponibili:**
- `command` - Esecuzione comandi
- `if` - Logica condizionale
- `loop` - Iterazioni
- `telegram` - Bot Telegram
- `linkedin` - Automazioni LinkedIn
- `email` - Gestione email
- `file` - Operazioni file
- `llm` - Integrazione LLM

## 📝 Esempio di Workflow YAML

```yaml
# Esempio: Bot Telegram con analisi AI
name: "AI Telegram Bot"
start_state: "listen"

variables:
  bot_token: "{TELEGRAM_BOT_TOKEN}"
  openai_key: "{OPENAI_API_KEY}"

states:
  listen:
    state_type: "telegram"
    bot_token: "{bot_token}"
    message_types: ["text"]
    output: "message_data"
    transition: "analyze"

  analyze:
    state_type: "llm"
    provider: "openai"
    model: "gpt-4"
    api_key: "{openai_key}"
    prompt: "Analizza questo messaggio: {message_data.text}"
    output: "analysis"
    transition: "respond"

  respond:
    state_type: "telegram"
    bot_token: "{bot_token}"
    chat_id: "{message_data.chat_id}"
    message: "Analisi: {analysis}"
    transition: "end"

  end:
    state_type: "end"
```

## 🔌 Sistema Plugin

### Plugin Disponibili
- **Comunicazione:** Telegram, Email, Slack
- **Social:** LinkedIn, Facebook, Twitter
- **AI/ML:** OpenAI, Anthropic, Ollama
- **Data:** RSS, Web Scraping, Database
- **Utility:** File Operations, HTTP Requests

### Creazione Plugin Custom
```python
# Esempio plugin custom
from flow.states.base_state import BaseState, STATE_REGISTRY

class CustomState(BaseState):
    def execute(self, variables):
        # Logica del plugin
        result = self.do_something()
        variables[self.config.get('output', 'result')] = result
        return self.config.get('transition', 'end')

# Registrazione automatica
STATE_REGISTRY['custom'] = CustomState
```

## 🐳 Docker Setup Completo

### docker-compose.yml (Root Level)
```yaml
version: '3.8'

services:
  # Backend API
  api:
    build: ./intellyhub-be
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/intellyhub
    depends_on:
      - db
    volumes:
      - ./intellyhub-be:/app
      - /var/run/docker.sock:/var/run/docker.sock

  # Database
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=intellyhub
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data

  # Frontend (opzionale per prod)
  frontend:
    build: ./intellyhub-fe
    ports:
      - "3000:3000"
    environment:
      - VITE_API_URL=http://localhost:5000
    volumes:
      - ./intellyhub-fe:/app

  # Worker Engine
  worker:
    build: ./ai-automation-fsm-py
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./ai-automation-fsm-py:/app
      - /var/run/docker.sock:/var/run/docker.sock

volumes:
  db_data:
```

## 🔐 Configurazione Ambiente

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql+psycopg2://user:pass@db:5432/intellyhub

# Security
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# Kubernetes
KUBECONFIG=/root/.kube/config
FSM_EXECUTOR_IMAGE=fsm-executor:latest

# AI Services
OPENAI_API_KEY=sk-your-openai-key

# Billing (Stripe)
STRIPE_SECRET_KEY=sk_test_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key
```

### Worker (.env)
```bash
# AI Services
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key

# Social Media
TELEGRAM_BOT_TOKEN=your-telegram-token
LINKEDIN_EMAIL=your-linkedin-email
LINKEDIN_PASSWORD=your-linkedin-password

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## 📊 Monitoraggio e Debugging

### Logs
```bash
# Backend logs
docker-compose logs -f api

# Worker logs
docker-compose logs -f worker

# Database logs
docker-compose logs -f db
```

### Health Checks
```bash
# API Health
curl http://localhost:5000/api/health

# Database Connection
curl http://localhost:5000/api/version

# Metrics (Prometheus)
curl http://localhost:5000/api/metrics
```

## 🧪 Testing

### Backend Tests
```bash
cd intellyhub-be
python -m pytest tests/
```

### Frontend Tests
```bash
cd intellyhub-fe
npm run test
npm run test:coverage
```

### Worker Tests
```bash
cd ai-automation-fsm-py
python -m pytest test/
```

## 🚀 Deployment

### Kubernetes Deployment
```bash
# Build images
docker build -t intellyhub-api ./intellyhub-be
docker build -t intellyhub-worker ./ai-automation-fsm-py

# Deploy to K8s
kubectl apply -f k8s/
```

### Production Environment
- **Backend:** Gunicorn + Nginx
- **Frontend:** Static build servito da CDN
- **Database:** PostgreSQL cluster
- **Worker:** Kubernetes Jobs
- **Monitoring:** Prometheus + Grafana

## 📈 Metriche Business

### KPI Tecnici
- **Uptime:** >99.9%
- **Response Time:** <200ms (API)
- **Plugin Availability:** >99%

### KPI Business
- **Monthly Active Users (MAU)**
- **Workflow Executions per Month**
- **Plugin Downloads**
- **Customer Acquisition Cost (CAC)**
- **Monthly Recurring Revenue (MRR)**

## 🔗 Link Utili

- **Documentazione API:** http://localhost:5000/api/docs
- **Frontend Dev:** http://localhost:3000
- **Grafana Dashboard:** http://localhost:3001
- **Plugin Repository:** https://github.com/kuduk/intellyhub-plugins

### Coding Standards
- **Backend:** PEP 8 (Python), Black formatter
- **Frontend:** ESLint + Prettier
- **Commit:** Conventional Commits
