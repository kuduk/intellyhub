# 🚀 IntellyHub

**IntellyHub** è una piattaforma enterprise per l'automazione dei processi aziendali con intelligenza artificiale, sistema di plugin dinamico e architettura cloud-native scalabile.

## ✨ Caratteristiche Principali

- 🤖 **AI-Powered Automation**: Integrazione completa con OpenAI e LangChain
- 🔌 **Sistema Plugin Dinamico**: Estendibilità infinita tramite plugin distribuiti
- 👥 **Multi-Tenant**: Isolamento completo tra utenti e organizzazioni
- 💰 **Billing Enterprise**: Gestione completa sottoscrizioni con Stripe
- 🔒 **Security Advanced**: Audit logging, protezione brute-force, JWT sicuri
- 📊 **Analytics & BI**: Dashboard analytics con metriche business avanzate
- ☸️ **Kubernetes Native**: Esecuzione flow in container isolati
- 🌐 **Architettura Moderna**: Frontend Vue.js + Backend Flask + Database PostgreSQL
- 🤖 **FSM Engine**: Motore Python per esecuzione flow con stati, listener e plugin

## 🏗️ Architettura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   Vue.js + Vite│◄──►│  Flask + SQLAlch│◄──►│   PostgreSQL    │
│   Port: 5173    │    │   Port: 5000    │    │   Port: 5432    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Kubernetes    │
                    │ Flow Execution  │
                    │   (Isolated)    │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │ FSM Executor    │
                    │ Python Engine   │
                    │ ai-automation-  │
                    │    fsm-py       │
                    └─────────────────┘
```

## 📁 Struttura del Progetto

```
IntellyHub/
├── 📂 intellyhub-be/           # Backend Flask API
│   ├── 📂 app/                 # Core application
│   │   ├── 📂 services/        # Business logic (Service Layer)
│   │   ├── 📂 middleware/      # Middleware personalizzati
│   │   ├── 📂 schemas/         # Data schemas
│   │   ├── 🐍 models.py        # Database models
│   │   ├── 🐍 auth.py          # Autenticazione JWT
│   │   ├── 🐍 flows.py         # Gestione flow automazione
│   │   ├── 🐍 billing.py       # Sistema billing Stripe
│   │   ├── 🐍 admin.py         # Panel amministrazione
│   │   ├── 🐍 plugins.py       # Sistema plugin dinamico
│   │   └── 🐍 analytics.py     # Business intelligence
│   ├── 📂 migrations/          # Database migrations
│   ├── 📂 tests/              # Suite di test completa
│   ├── 🐳 Dockerfile          # Container backend
│   └── 📋 requirements.txt    # Dipendenze Python
├── 📂 intellyhub-fe/           # Frontend Vue.js
│   ├── 📂 src/
│   │   ├── 📂 components/      # Componenti Vue
│   │   ├── 📂 pages/          # Pagine applicazione
│   │   ├── 📂 composables/    # Logic riusabile
│   │   ├── 📂 layouts/        # Layout templates
│   │   └── 📂 locales/        # Internazionalizzazione
│   ├── 📂 tests/              # Test frontend
│   ├── 🐳 Dockerfile          # Container frontend
│   └── 📦 package.json        # Dipendenze Node.js
├── 📂 ai-automation-fsm-py/   # 🚀 FSM Execution Engine
│   ├── 📂 flow/               # Core FSM Framework
│   │   ├── 📂 states/         # Tipi di stato (command, if, loop, etc.)
│   │   ├── 📂 listeners/      # Event listeners (email, webhook, RSS)
│   │   ├── 🐍 flow.py         # Parser YAML e Flow Engine
│   │   ├── 🐍 lazy_loader.py  # Sistema caricamento dinamico
│   │   └── 🐍 plugin_loader.py# Gestione plugin runtime
│   ├── 📂 diagrammi/          # Template e esempi YAML flows
│   ├── 📂 documentazione/     # Guide complete DSL e plugin
│   ├── 📂 test/              # Test suite per FSM engine
│   ├── 🐍 main.py            # Entry point con auto-restart
│   ├── 🐍 package_manager.py # Gestione dipendenze plugin
│   ├── 🐳 Dockerfile         # Container FSM executor
│   └── 📋 requirements.txt   # Dipendenze Python FSM
├── 🐳 docker-compose.yml      # Orchestrazione servizi
└── 📖 README.md               # Questa documentazione
```

## 🚀 Quick Start

### 1. Prerequisiti

```bash
# Verifica Docker e Docker Compose
docker --version          # >= 20.10
docker compose --version  # >= 2.0
```

### 2. Setup Ambiente

```bash
# Clone del repository
git clone https://github.com/kuduk/IntellyHub.git
cd IntellyHub

# Configura ambiente backend
cd intellyhub-be
cp .env.example .env
# ✏️ Modifica .env con le tue configurazioni
cd ..
```

### 3. Avvio Sistema

```bash
# Avvia tutti i servizi con build
docker compose up --build

# In modalità detached (background)
docker compose up -d --build

# Verifica stato servizi
docker compose ps
```

### 4. Inizializzazione Database

```bash
# Applica migrazioni database
docker compose exec api python3 -m flask db upgrade

# Popola piani di pricing
docker compose exec api python3 populate_plans.py

# Crea utente amministratore
docker compose exec api python3 setup_admin.py
```

### 5. Accesso alle Applicazioni

- 🌐 **Frontend**: http://localhost:5173
- 🔌 **API Backend**: http://localhost:5000
- 📚 **API Docs**: http://localhost:5000/api/docs
- 🗄️ **Database**: localhost:5432

## 🔧 Configurazione Avanzata

### Variabili d'Ambiente Principali

```bash
# === CORE CONFIGURATION ===
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=postgresql+psycopg2://user:pass@db:5432/intellyhub

# === STRIPE BILLING ===
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
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

### Configurazione Produzione

```bash
# Variabili specifiche produzione
FLASK_ENV=production
DEBUG=False
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
REDIS_URL=redis://your-redis-host:6379/0
SENTRY_DSN=https://your-sentry-dsn
```

## 📊 Funzionalità Enterprise

### 💰 Sistema Billing Completo
- **Piani di Pricing**: Free, Standard, Business, Scale, Enterprise
- **Sottoscrizioni Ricorrenti**: Gestione automatica con Stripe
- **Add-on Pod**: Risorse aggiuntive per scaling
- **Fatturazione Automatica**: Invoice e payment tracking
- **Analytics Revenue**: MRR, churn rate, conversion metrics

### 🔒 Sicurezza Enterprise-Grade
- **Password Policy**: Lunghezza minima, complessità obbligatoria
- **Protezione Brute Force**: Blocco IP automatico dopo 5 tentativi
- **JWT Sicuri**: Claims avanzati con validazione IP/Browser
- **Audit Logging**: Log completo di tutte le operazioni
- **Rate Limiting**: Protezione API con Redis

### 👑 Panel Amministrazione
- **Dashboard KPI**: Metriche business in real-time
- **Gestione Utenti**: CRUD completo con ruoli avanzati
- **Sottoscrizioni**: Modifica piani e billing management
- **Analytics**: Conversion rate, churn, revenue breakdown
- **Security Alerts**: Monitoraggio eventi sospetti
- **Audit Trail**: Export log per compliance

### 🔌 Sistema Plugin Dinamico
- **Repository GitHub**: Plugin distribuiti automaticamente
- **Installazione Automatica**: Analisi YAML per suggerire plugin
- **Configurazione Per-Flow**: Plugin isolati per ogni automazione
- **Hot-Reload**: Aggiornamento plugin senza restart

### 📈 Analytics & Business Intelligence
- **Metriche Business**: MRR, ARPU, conversion rate, churn
- **Utilizzo Sistema**: Pod utilization, API metrics
- **Export Dati**: CSV/Excel per analisi esterne
- **Dashboard Real-time**: KPI aggiornati automaticamente

## 🧪 Testing

### Backend Testing

```bash
# Entra nel container backend
docker compose exec api bash

# Run test suite completa
python -m pytest

# Test con coverage
python -m pytest --cov=app --cov-report=html

# Test specifici
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/security/
```

### Frontend Testing

```bash
# Entra nel container frontend
docker compose exec frontend sh

# Run test suite
npm test

# Test con UI
npm run test:ui

# Test con coverage
npm run test:coverage

# Test in watch mode
npm run test:watch
```

## 🤖 FSM Engine (ai-automation-fsm-py)

Il **FSM Engine** è il cuore dell'automazione di IntellyHub, un potente motore Python che esegue i flow basati su macchine a stati finiti (FSM) definiti in YAML.

### 🎯 Caratteristiche del FSM Engine

- **📝 DSL YAML**: Linguaggio specifico per definire workflow complessi
- **🔄 Stati e Transizioni**: Architettura a stati finiti con transizioni dinamiche  
- **👂 Event Listeners**: Supporto per eventi esterni (email, webhook, RSS, Telegram)
- **🔌 Plugin System**: Estensibilità completa con caricamento dinamico
- **🧠 AI Integration**: Integrazione nativa con LLM (OpenAI, Ollama)
- **📊 Variable System**: Gestione avanzata variabili e interpolazione
- **🔄 Auto-Restart**: Meccanismo automatico di restart e recovery
- **🧪 Test Coverage**: Suite di test completa per ogni componente

### 📋 Tipi di Stato Disponibili

| Tipo di Stato | Descrizione | Esempi d'Uso |
|---------------|-------------|---------------|
| **command** | Esecuzione comandi shell | Script, deploy, file operations |
| **if** | Logica condizionale | Branching, validazione dati |
| **loop** | Iterazione su collezioni | Batch processing, data transformation |
| **llm_agent** | Integrazione AI/LLM | ChatGPT, Ollama, reasoning |
| **telegram-bot** | Bot Telegram | Notifiche, interactive chat |
| **facebook** | API Facebook | Social media automation |
| **linkedin** | Scraping LinkedIn | Lead generation, talent search |
| **rss_reader** | Feed RSS/Atom | News monitoring, content aggregation |
| **text_to_speech** | Text-to-Speech | Audio notifications, accessibility |
| **file** | File operations | Read/write/move files |
| **end** | Terminazione flow | Success/failure completion |

### 👂 Event Listeners Supportati

| Listener | Descrizione | Trigger Events |
|----------|-------------|----------------|
| **email** | Monitoraggio email IMAP | Nuove email, filtri mittente/oggetto |
| **webhook** | Server webhook HTTP | POST requests, payload processing |
| **rss** | Feed RSS/Atom | Nuovi articoli, keyword matching |
| **telegram** | Bot Telegram | Messaggi, comandi, inline queries |
| **directory** | File system watcher | File creati/modificati/eliminati |
| **mqtt** | Message broker MQTT | Topic subscription, IoT events |

### 🔧 Esempio di Flow YAML

```yaml
# Esempio: Monitoraggio RSS con notifica Telegram
name: "RSS News Monitor"
description: "Monitora feed RSS e invia notifiche Telegram per news rilevanti"

# Variabili globali
variables:
  telegram_bot_token: "{TELEGRAM_BOT_TOKEN}"
  telegram_chat_id: "{TELEGRAM_CHAT_ID}"
  keywords: ["AI", "automation", "python"]

# Listener per eventi RSS
listener:
  type: rss
  url: "https://feeds.feedburner.com/oreilly/radar"
  check_interval: 300  # 5 minuti

# Stato iniziale
start_state: "process_article"

states:
  # Processa nuovo articolo RSS
  process_article:
    state_type: if
    condition: "{event.title} contains any {keywords}"
    true_transition: "send_notification"
    false_transition: "end"
  
  # Invia notifica Telegram
  send_notification:
    state_type: telegram-bot
    bot_token: "{telegram_bot_token}"
    chat_id: "{telegram_chat_id}"
    message: |
      🔔 **Nuovo Articolo Rilevante**
      
      **Titolo**: {event.title}
      **Autore**: {event.author}
      **Link**: {event.link}
      
      **Summary**: {event.summary[:200]}...
    transition: "end"
  
  # Terminazione
  end:
    state_type: end
```

### 🚀 Esecuzione Flow

```bash
# Esecuzione diretta
cd ai-automation-fsm-py
python main.py diagrammi/example_rss_monitor.yaml

# Con parametri aggiuntivi
python main.py diagrammi/telegram_bot.yaml --verbose --max-steps 50

# In modalità daemon (background)
nohup python main.py diagrammi/monitoring_flow.yaml > flow.log 2>&1 &
```

### 🧪 Testing FSM Engine

```bash
cd ai-automation-fsm-py

# Test suite completa
pytest

# Test con coverage
pytest --cov=flow --cov-report=html

# Test specifici per stati
pytest test/test_states/ -v

# Test integrazione
pytest test/test_integration.py -v
```

### 🔌 Sistema Plugin Avanzato

Il FSM Engine supporta plugin dinamici per estendere le funzionalità:

```bash
# Gestione plugin tramite package manager
python package_manager.py install telegram-advanced
python package_manager.py list
python package_manager.py update all

# Plugin vengono caricati automaticamente da:
# - Directory locale plugins/
# - Repository GitHub intellyhub-plugins
# - Package PyPI con prefisso intellyhub-plugin-
```

### 📚 Documentazione FSM

- **[YAML_DSL_COMPLETE_GUIDE.md](ai-automation-fsm-py/documentazione/YAML_DSL_COMPLETE_GUIDE.md)** - Guida completa DSL YAML
- **[PLUGIN_SYSTEM.md](ai-automation-fsm-py/documentazione/PLUGIN_SYSTEM.md)** - Architettura sistema plugin  
- **[PLUGIN_CREATION_GUIDE.md](ai-automation-fsm-py/documentazione/PLUGIN_CREATION_GUIDE.md)** - Come creare plugin custom
- **[LAZY_LOADING_SYSTEM.md](ai-automation-fsm-py/documentazione/LAZY_LOADING_SYSTEM.md)** - Sistema caricamento dinamico

## 📚 API Reference

### Autenticazione

```bash
# Registrazione utente
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123!"}'

# Login utente
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123!"}'
```

### Flow Management

```bash
# Lista flow dell'utente
curl -X GET http://localhost:5000/api/flows \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Crea nuovo flow
curl -X POST http://localhost:5000/api/flows \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Flow", "yaml_content": "..."}'

# Esegui flow
curl -X POST http://localhost:5000/api/flows/FLOW_ID/execute \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Billing & Subscriptions

```bash
# Lista piani disponibili
curl -X GET http://localhost:5000/api/billing/plans

# Sottoscrizione corrente
curl -X GET http://localhost:5000/api/billing/subscription \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Crea sessione checkout
curl -X POST http://localhost:5000/api/billing/create-checkout-session \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"plan_name": "standard"}'
```

### Analytics & Admin

```bash
# Dashboard admin (solo admin)
curl -X GET http://localhost:5000/api/admin/dashboard \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"

# Conversion rate
curl -X GET http://localhost:5000/api/analytics/conversion-rate \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"

# Export utenti
curl -X GET http://localhost:5000/api/exports/users?format=csv \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"
```

## 🔍 Monitoraggio e Osservabilità

### Metriche Prometheus

```bash
# Endpoint metriche (formato Prometheus)
curl http://localhost:5000/api/metrics

# Health check dettagliato
curl http://localhost:5000/api/health?detailed=true

# System metrics (admin only)
curl -X GET http://localhost:5000/api/system-metrics \
  -H "Authorization: Bearer ADMIN_JWT_TOKEN"
```

### Logging e Debug

```bash
# Visualizza logs in real-time
docker compose logs -f api
docker compose logs -f frontend

# Logs specifici per servizio
docker compose logs api --tail=100
docker compose logs db --since=1h
```

## 🛠️ Development

### Setup Ambiente Sviluppo

```bash
# Backend development
cd intellyhub-be
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt

# Frontend development
cd intellyhub-fe
npm install
npm run dev
```

### Hot Reload

Il docker-compose.yml è configurato per il development con hot-reload automatico:

- **Backend**: Modifiche in `intellyhub-be/` ricaricano automaticamente Flask
- **Frontend**: Modifiche in `intellyhub-fe/src/` ricompilano automaticamente Vite
- **Database**: Dati persistenti tramite volume Docker

### Database Migrations

```bash
# Crea nuova migrazione
docker compose exec api python3 -m flask db migrate -m "Descrizione migrazione"

# Applica migrazioni
docker compose exec api python3 -m flask db upgrade

# Rollback migrazione
docker compose exec api python3 -m flask db downgrade
```

## 🚢 Deployment Produzione

### Docker Swarm

```yaml
# docker-stack.yml
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
  frontend:
    image: intellyhub/frontend:latest
    deploy:
      replicas: 2
```

### Kubernetes

```yaml
# k8s-deployment.yml
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
```

## 📈 Performance & Scaling

### Metriche di Performance
- **Response Time API**: < 200ms (p95)
- **Database Queries**: < 50ms (p95)
- **Flow Execution**: < 30s (automazioni standard)
- **Concurrent Users**: 1000+ utenti simultanei
- **Pod Capacity**: 100+ pod in parallelo per piano Enterprise

### Ottimizzazioni
- **Database**: Connection pooling, query optimization, indexes
- **API**: Rate limiting, caching Redis, response compression
- **Frontend**: Code splitting, lazy loading, asset optimization
- **Infrastructure**: Load balancing, CDN, auto-scaling

## 🤝 Contributing

```bash
# Fork del repository
gh repo fork kuduk/IntellyHub

# Crea branch feature
git checkout -b feature/nome-feature

# Commit changes
git commit -m "feat: descrizione feature"

# Push e crea PR
git push origin feature/nome-feature
gh pr create --title "Feature: Nome Feature"
```

### Standards di Qualità
- ✅ **Test Coverage**: >= 80% per backend, >= 70% per frontend  
- ✅ **Code Quality**: ESLint/Pylint passing
- ✅ **Security**: Audit automatico delle dipendenze
- ✅ **Documentation**: JSDoc/Sphinx per funzioni pubbliche

