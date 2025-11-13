# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

IntellyHub is an enterprise AI-powered business process automation platform with a dynamic plugin system and cloud-native architecture. The project is a **monorepo** with 3 main Git submodules:

- **Backend** (`intellyhub-be`): Flask + SQLAlchemy API (container: `api`)
- **Frontend** (`intellyhub-fe`): Vue.js 3 + Vite + Vuetify (container: `frontend`)
- **FSM Engine** (`ai-automation-fsm-py`): Python finite state machine executor
- **Database**: PostgreSQL 15 (container: `db`)

## Architecture

### Containerized Microservices
- All components managed via Docker Compose from the root directory
- Backend exposes REST API on port 5000
- Frontend development server on port 5173
- Database on port 5432

### Flow Execution Model
1. User creates/edits flow YAML in the frontend visual editor (Vue Flow)
2. Backend validates and stores YAML in `flow` and `flow_version` tables
3. On execution: Backend creates Kubernetes Job with FSM executor container
4. FSM engine parses YAML, resolves plugins/dependencies dynamically, executes states
5. Results/logs streamed back via polling endpoint

### Key Architectural Patterns

#### Backend: Service Layer Architecture
- **Controllers** (Flask blueprints) → **Services** → **Models** → **Database**
- All services inherit from `BaseService` for audit logging
- JWT authentication with `@jwt_required()` decorator
- Multi-tenant isolation: all data scoped by `user_id`

#### Frontend: Composition API with Composables
- **Pages** → **Layouts** → **Components** → **Composables** (state management)
- Key composables: `useAuth`, `useFlows`, `usePlugins`, `useAutomationState`
- Real-time automation status polling every 5 seconds
- Role-based permissions via `usePermissions`

#### FSM Engine: Dynamic State Machine with Metaclass Registry
- **FlowDiagram** parses YAML → **StateRegistry** executes states → **PluginLoader** manages plugins
- Metaclass-based auto-registration (`StateMeta`, `ListenerMeta`)
- Lazy loading: plugins loaded only when needed (NOT at startup)
- Auto-restart mechanism for dependency installation

## Common Commands

### Docker & Services

```bash
# Start all services from root directory
docker compose up -d --build

# Verify services running
docker compose ps

# View logs in real-time
docker compose logs -f api          # Backend logs
docker compose logs -f frontend     # Frontend logs
docker compose logs -f db           # Database logs

# Stop all services
docker compose down

# Reset everything (DANGER: deletes volumes)
docker compose down -v
docker compose up -d --build

# Enter container shell
docker compose exec api bash        # Backend shell
docker compose exec frontend sh     # Frontend shell
```

### Database

**CRITICAL: Database Migrations**

**ALWAYS use Flask commands via Docker** for database operations. NEVER create migrations manually or run Flask commands outside of Docker.

```bash
# Apply migrations (ALWAYS run after git pull)
docker compose exec api python3 -m flask db upgrade

# Create new migration (review before committing!)
# Flask will auto-generate the migration based on model changes
docker compose exec api python3 -m flask db migrate -m "Description"

# Rollback last migration
docker compose exec api python3 -m flask db downgrade

# Initialize database with subscription plans
docker compose exec api python3 populate_plans.py

# Create admin user (interactive)
docker compose exec api python3 setup_admin.py

# Check database connection
docker compose exec db pg_isready -U user -d intellyhub

# Access psql console
docker compose exec db psql -U user -d intellyhub
```

### Backend Testing

```bash
# Enter backend container
docker compose exec api bash

# Run full test suite
python -m pytest

# Run with coverage
python -m pytest --cov=app --cov-report=html

# Run specific test types
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/security/
```

### Frontend Testing

```bash
# Enter frontend container
docker compose exec frontend sh

# Run tests
npm test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### FSM Engine (ai-automation-fsm-py)

```bash
cd ai-automation-fsm-py

# Execute a flow (YAML workflow)
python main.py diagrammi/example_flow.yaml

# With verbose output and step limit
python main.py diagrammi/telegram_bot.yaml --verbose --max-steps 50

# Run in background (daemon mode)
nohup python main.py diagrammi/monitoring_flow.yaml > flow.log 2>&1 &

# Plugin management
python main.py plugins list                    # List installed plugins
python main.py plugins install [plugin_id]     # Install specific plugin
python main.py plugins freeze                  # Save plugin versions
python main.py plugins uninstall <plugin_id>   # Remove plugin

# Testing
pytest                                         # Run all tests
pytest --cov=flow --cov-report=html           # With coverage report
pytest test/test_states/ -v                   # Test specific states
pytest test/test_integration.py -v            # Integration tests

# Performance Optimization (build optimized Docker image)
./build-fsm-executor.sh                       # Build image with pre-installed dependencies
                                               # Reduces flow startup from 10+ min to ~5 sec
                                               # Image size: ~4-5 GB (includes torch, langchain, etc.)
```

### Performance Optimization

**Problem:** Flow execution with heavy plugins (llm-agent, google-sheets) takes 10+ minutes to start due to on-demand dependency installation.

**Solution:** Pre-built Docker image with dependencies + Persistent cache.

```bash
# 1. Build optimized FSM executor image (one-time, takes 10-15 min)
cd ai-automation-fsm-py
./build-fsm-executor.sh

# 2. Deploy pip cache PersistentVolumeClaim
kubectl apply -f intellyhub-be/k8s/pip-cache-pvc.yaml

# 3. Configure backend to use new image
echo "FSM_EXECUTOR_IMAGE=fsm-executor:latest" >> intellyhub-be/.env
docker compose restart api

# Result: Flow startup reduced from 10+ minutes to ~5 seconds! 🚀
```

**See:** `ai-automation-fsm-py/documentazione/PERFORMANCE_OPTIMIZATION.md` for full details.

### Stripe Testing

```bash
# Start Stripe webhook listener for local testing
./stripe-tunnel.sh

# Forwards webhooks to http://localhost:5000/api/billing/webhook
# Copy the generated STRIPE_WEBHOOK_SECRET to intellyhub-be/.env
# Requires: stripe CLI installed and logged in
```

### Git Submodules

```bash
# Update all submodules to latest
git submodule update --init --recursive

# Update specific submodule
cd intellyhub-be && git pull origin master && cd ..
git add intellyhub-be
git commit -m "Update backend submodule"

# Check submodule status
git submodule status
```

## Microservices Management

IntellyHub supporta la gestione di microservizi sia locali (Kubernetes) che remoti (cloud) con risoluzione automatica delle dipendenze per i flow.

### Overview

- **Zero-Configuration**: I plugin dichiarano dipendenze, il sistema risolve e inietta automaticamente le connessioni
- **Auto-Deploy**: Microservizi locali deployati automaticamente in Kubernetes quando necessario
- **Health Checks**: Verifica automatica della disponibilità prima dell'esecuzione dei flow
- **Full Management**: CRUD operations, logs, scaling, restart via UI e API

### Architecture Components

**Backend:**
- `app/models.py`: Microservice, FlowMicroserviceDependency, MicroserviceHealthCheck models
- `app/services/dependency_resolver.py`: Risoluzione automatica dipendenze
- `app/k8s_microservice_manager.py`: Kubernetes deployment management
- `app/microservices.py`: REST API blueprint (12 endpoints)

**Frontend:**
- `src/composables/useMicroservices.ts`: State management
- `src/pages/MicroservicesManagement.vue`: Management UI completa
- Route: `/microservices`

### Key Features

#### 1. Dependency Resolution
Il sistema risolve automaticamente le dipendenze quando un flow viene eseguito:

```python
# In app/flows.py execute_flow endpoint:
resolver = DependencyResolver(user_id=user_id)
resolution = resolver.resolve_flow_dependencies(flow_id, flow_yaml)
env_vars = resolution['injected_vars']  # NEO4J_BOLT_URL, REDIS_URL, ecc.

# Variabili iniettate nel Kubernetes Job
create_flow_job(user_id, flow_id, yaml_content, env_vars=env_vars)
```

#### 2. Plugin Manifest Dependencies
I plugin dichiarano le loro dipendenze:

```json
{
  "name": "mcp-neo4j",
  "dependencies": {
    "services": [{
      "type": "neo4j",
      "required": true,
      "prefer": "remote",
      "fallback": ["local"],
      "connection_vars": {
        "bolt_url": "NEO4J_BOLT_URL",
        "username": "NEO4J_USERNAME",
        "password": "NEO4J_PASSWORD"
      },
      "health_check": {
        "type": "tcp",
        "port": 7687
      }
    }]
  }
}
```

#### 3. Zero-Config Flows
I flow non necessitano di configurazione manuale:

```yaml
states:
  query_graph:
    state_type: mcp_neo4j
    # NO neo4j_url, username, password needed!
    # Automatically injected: NEO4J_BOLT_URL, NEO4J_USERNAME, NEO4J_PASSWORD
    query: "MATCH (n:Person) RETURN n LIMIT 10"
    output: graph_data
```

### API Endpoints

```bash
# List microservices
GET /api/microservices?location=local&service_type=neo4j

# Get details with deployment status
GET /api/microservices/{id}

# Create (auto-deploys if local)
POST /api/microservices
{
  "name": "Neo4j Local",
  "service_type": "neo4j",
  "location": "local",
  "connection_info": {...},
  "config": {...}
}

# Update
PUT /api/microservices/{id}

# Delete (with dependency check)
DELETE /api/microservices/{id}

# Operations
POST /api/microservices/{id}/restart
POST /api/microservices/{id}/scale {"replicas": 3}
GET  /api/microservices/{id}/logs?tail=100
GET  /api/microservices/{id}/health?limit=10

# Bulk operations
POST /api/microservices/yaml/import
GET  /api/microservices/yaml/export

# Statistics
GET /api/microservices/stats
```

### Frontend Features

**Management UI** (`/microservices`):
- List with filters (location, type, status, search)
- Create/Edit dialogs with JSON validation
- Details viewer with tabs:
  - Info: Complete details and configuration
  - Status: Deployment status, replicas, pods (local only)
  - Health: Timeline of health checks
  - Logs: Streaming logs viewer
  - Dependencies: Flows using this microservice
- Operations: Restart, Scale (slider 0-10 replicas)
- Import/Export YAML
- Statistics dashboard

### Microservices Configuration

**Example: microservices.yaml**
```yaml
version: "1.0"

microservices:
  - id: neo4j-local
    name: "Neo4j Graph Database"
    type: neo4j
    location: local

    config:
      image: neo4j:5.15
      replicas: 1
      ports:
        - name: bolt
          containerPort: 7687
          servicePort: 7687
      volumes:
        - name: neo4j-data
          mountPath: /data
          size: 20Gi
      env:
        - name: NEO4J_AUTH
          value: "neo4j/{NEO4J_PASSWORD}"
      healthCheck:
        type: tcp
        port: 7687
        initialDelay: 30
        period: 10

    connection:
      bolt_url: "bolt://neo4j-local.intellyhub.svc.cluster.local:7687"
      username: "neo4j"
      password: "{NEO4J_PASSWORD}"

    tags: ["database", "graph", "local"]
    cost_estimate: "$25/month"
```

### Testing Microservices

```bash
# Apply migration
docker compose exec api flask db upgrade

# Navigate to frontend
# http://localhost:5173/microservices

# Create a microservice via UI or API
curl -X POST http://localhost:5000/api/microservices \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @microservice.json

# Create a flow using the microservice
# The system will automatically:
# 1. Detect plugin dependencies
# 2. Find matching microservice
# 3. Deploy if local and not running
# 4. Verify health
# 5. Inject connection variables
# 6. Execute flow

# Check deployment status
kubectl get deployments -n intellyhub
kubectl get pods -n intellyhub

# View microservice details in UI
# http://localhost:5173/microservices → Click on microservice → Details tabs
```

### Documentation

- **Complete Guide**: `MICROSERVICES_FEATURE_COMPLETE.md`
- **Examples**: `examples/microservices.yaml`, `examples/plugin-manifest-with-dependencies.json`
- **Flow Example**: `examples/flow-with-microservice-dependencies.yaml`

## Project Structure

### Backend (intellyhub-be/)

**Key Files:**
- `app/__init__.py` - Application factory with blueprint registration
- `app/models.py` - SQLAlchemy models (User, Flow, FlowVersion, Subscription, Plan, etc.)
- `app/auth.py` - JWT authentication endpoints (`/api/auth/login`, `/api/auth/register`)
- `app/flows.py` - Flow CRUD and execution endpoints (`/api/flows/*`)
- `app/billing.py` - Stripe integration (`/api/billing/*`, webhook handler)
- `app/plugins.py` - Dynamic plugin system (`/api/plugins/*`)
- `app/admin.py` - Admin panel with KPI dashboard (`/api/admin/*`)
- `app/analytics.py` - Business intelligence (`/api/analytics/*`)
- `app/chat.py` - AI assistant chat endpoint
- `app/security.py` - Brute force protection, audit logging
- `app/k8s_executor.py` - Kubernetes job launcher for flow execution

**Service Layer** (`app/services/`):
- `base_service.py` - Base class with audit logging (inherit from this!)
- `flow_service.py` - Flow execution, versioning, status tracking
- `user_service.py` - User CRUD and authentication
- `subscription_service.py` - Subscription lifecycle management
- `monitoring_service.py` - System health and metrics

### Frontend (intellyhub-fe/)

**Structure:**
- `src/components/` - Reusable Vue components
- `src/pages/` - Application pages/views
- `src/composables/` - Composition API state management
  - `useAuth.ts` - Authentication state (token in localStorage)
  - `useFlows.ts` - Flow management
  - `usePlugins.ts` - Plugin state
  - `useAutomationState.ts` - Real-time flow status polling (5s interval)
  - `usePermissions.ts` - Role-based access control
- `src/layouts/` - Layout templates (MainLayout, AuthLayout)
- `src/locales/` - i18n translations (it.json, en.json)
- `src/router.ts` - Vue Router configuration

**Key Technologies:**
- Vue 3 Composition API
- Vuetify 3 (Material Design components)
- Monaco Editor (YAML editing with syntax highlighting)
- Vue Flow (visual flow diagram editor)
- Chart.js + vue-chartjs (analytics charts)
- Socket.IO client (real-time updates)
- Axios (HTTP client)

**CRITICAL: Frontend API Endpoints**

**ALWAYS use relative paths** for API calls in the frontend. The Vite dev server has a proxy configured to forward requests to the backend.

**How it works:**
1. **Browser** makes request with relative URL: `/api/microservices`
2. **Vite dev server** (inside frontend container) intercepts the request
3. **Vite proxy** forwards to backend: `http://api:5000/api/microservices` (Docker internal network)
4. **Backend** processes and responds
5. **Browser** receives the response

**Correct axios configuration** (`src/axios.ts`):
```typescript
const instance = axios.create({
  baseURL: '', // Empty string - use Vite proxy for all requests
})
```

**Correct API calls** (in composables):
```typescript
// ✅ CORRECT - Relative path
await axios.get('/api/microservices')
await axios.post('/api/flows', data)

// ❌ WRONG - Absolute URL (bypasses proxy)
await axios.get('http://api:5000/api/microservices')
await axios.get('http://localhost:5000/api/flows')
```

**Environment variable** (`docker-compose.yml`):
```yaml
environment:
  - VITE_API_BASE_URL=http://api:5000  # Used by Vite proxy (server-side)
```

**Important:** `VITE_API_BASE_URL` is used by the Vite proxy server (inside Docker container), NOT by the browser. It must use the Docker service name `api`, not `localhost`.

### FSM Engine (ai-automation-fsm-py/)

**Core Components:**
- `main.py` - Entry point with auto-restart mechanism
- `flow/flow.py` - FlowDiagram class (YAML parser and execution engine)
- `flow/states/` - Built-in state types (command, if, loop, switch, file, end, etc.)
  - `base_state.py` - BaseState with metaclass auto-registration
  - Plugins copied here on installation
- `flow/listeners/` - Event listeners (email, webhook, RSS, telegram, directory, MQTT)
  - `base_listener.py` - BaseListener with metaclass auto-registration
- `flow/plugin_loader.py` - Dynamic plugin loading (lazy + on-demand installation)
- `flow/lazy_loader.py` - Performance optimization (load plugins only when used)
- `package_manager.py` - Plugin CLI manager
- `diagrammi/` - Example YAML workflows
- `documentazione/` - Complete DSL documentation

**Plugin System:**
- `intellyhub-plugins/` - Plugin repository (Git submodule)
  - Each plugin has `manifest.json` + entry file + optional icon
  - Auto-installation: analyze YAML → suggest plugins → pip install requirements
  - Plugins auto-register via metaclasses (NO manual registration needed)

## Database Schema (PostgreSQL)

### Core Tables
- **`user`** - Authentication and user profiles
  - Primary key: `id` (integer, autoincrement)
  - Relationships: flows, subscriptions, variables, secrets
  - Cascade delete: removes all user data on deletion

- **`flow`** - Flow definitions with versioning
  - Primary key: `id` (UUID)
  - Foreign key: `user_id` (CASCADE delete)
  - Fields: `thread_id` (AI chat context), `current_version`
  - Relationships: `flow_version`, `flow_plugins`

- **`flow_version`** - Version control for flows
  - Primary key: `id` (integer)
  - Foreign key: `flow_id` (CASCADE delete)
  - Unique constraint: `(flow_id, version)`
  - Fields: `content` (YAML text), `created_at`

- **`variable`** - User-defined variables for flow execution
  - Scoped by `user_id`
  - Used for variable interpolation in YAML

- **`secret`** - Encrypted secret storage
  - Scoped by `user_id`
  - For sensitive data (API keys, passwords)

- **`plugin`** - Available plugins with manifests
  - Fields: `manifest` (JSON), `installed_at`
  - Repository synced from GitHub

- **`flow_plugin`** - Plugin installations per flow
  - Foreign keys: `flow_id`, `plugin_id`
  - Fields: `config` (JSON), `enabled` (boolean)

### Billing Tables
- **`plan`** - Subscription plans
  - Fields: `stripe_price_id`, `max_pods`, `max_flow_executions_per_month`

- **`subscription`** - User subscriptions
  - Fields: `stripe_subscription_id`, `status`, `total_pods`, `max_total_pods`
  - Relationship: one-to-one with `user`

- **`usage`** - Usage tracking for billing
  - Tracks pod usage, API calls, flow executions

- **`invoice`** - Billing invoices
  - Fields: `stripe_invoice_id`, `amount_paid`, `pdf_url`

### Important Constraints
- **Foreign key cascades**: User deletion removes all flows, subscriptions, variables
- **Unique constraints**: Flow versions must be unique per flow
- **Indexing**: Foreign keys indexed for performance

## YAML DSL (Flow Definition Language)

### Required Sections
```yaml
start_state: "initial_state"  # Entry point

states:
  state_name:
    state_type: "command|if|loop|switch|end|llm_agent|etc"
    # state-specific parameters
    transition: "next_state"  # or use success_transition/error_transition
```

### Optional Sections
```yaml
# Global variables (interpolated as {variable_name})
variables:
  api_key: "{OPENAI_API_KEY}"  # From environment or user variables
  threshold: 10

# Event listener (triggers flow execution)
listener:
  type: "email|webhook|rss|telegram|directory|mqtt|mcp|a2a"
  # listener-specific config

# Safety limit
max_steps: 100  # Prevents infinite loops (default: 100)
```

### Available State Types
- **command** - Shell, HTTP, MQTT, email, eval
- **if** - Conditional branching (`condition`, `true_transition`, `false_transition`)
- **loop** - Iteration (`for` or `while` mode)
- **switch** - Multi-way branching (like switch/case)
- **file** - File operations (read, write, append, delete)
- **end** - Flow termination
- **llm_agent** - AI/LLM integration (OpenAI, Ollama)
- **telegram-bot** - Telegram messaging
- **facebook**, **linkedin**, **wechat** - Social media plugins
- **rss_reader** - RSS feed processing
- **text_to_speech** - Audio conversion
- **google-sheets** - Spreadsheet integration
- **mcp**, **a2a** - Protocol integrations

### Available Listeners
- **email** - IMAP monitoring (vars: `event.sender`, `event.subject`, `event.body`)
- **webhook** - HTTP server (vars: `event.method`, `event.headers`, `event.body`)
- **rss** - RSS feed (vars: `event.title`, `event.link`, `event.description`)
- **telegram** - Telegram bot (vars: `event.chat_id`, `event.message`)
- **directory** - File watcher (vars: `event.file_path`, `event.event_type`)
- **mqtt** - MQTT broker (vars: `event.topic`, `event.payload`)
- **mcp**, **a2a** - Protocol listeners

### Variable Interpolation
- Use `{variable_name}` anywhere in YAML
- Recursive interpolation supported
- Sources: environment vars, user variables, event context
- Example: `message: "Hello {user_name}, your balance is {balance}"`

### Common Patterns
```yaml
# Logging (available in ALL states)
log:
  message: "Processing {item}"
  level: "info"  # debug|info|warning|error

# Error handling
success_transition: "next_state"
error_transition: "error_handler"

# Conditional logic
state_type: if
condition: "{temperature} > 30"
true_transition: "send_alert"
false_transition: "continue"

# Loops
state_type: loop
mode: for
items: "{user_list}"
transition: "process_user"
```

## Environment Variables

### Backend (.env in intellyhub-be/)
```bash
# Core
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql+psycopg2://user:pass@db:5432/intellyhub

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_ASSISTANT_ID=asst_...

# Kubernetes
KUBECONFIG=/root/.kube/config
K8S_NAMESPACE=intellyhub-production
FSM_EXECUTOR_IMAGE=fsm-executor:latest

# Email (optional, for email listener)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Frontend (.env in intellyhub-fe/)
```bash
VITE_API_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
VITE_STRIPE_PUBLIC_KEY=pk_test_...
```

## Development Workflow

### Hot Reload Configuration
Docker Compose uses bind mounts for instant code reloading:
- **Backend**: Flask auto-reloads on changes in `intellyhub-be/app/`
- **Frontend**: Vite HMR recompiles on changes in `intellyhub-fe/src/`
- **Database**: Data persisted in Docker volume `db_data`

### Adding a Backend Endpoint
1. **Update model** (if needed) in `app/models.py`
   - Add new fields/relationships
2. **Create migration**: `docker compose exec api flask db migrate -m "Add feature X"`
3. **Review migration** in `migrations/versions/` (IMPORTANT: auto-generated but must be checked!)
4. **Apply migration**: `docker compose exec api flask db upgrade`
5. **Add service method** in `app/services/[feature]_service.py`
   - Inherit from `BaseService` for audit logging
   - Implement business logic here (NOT in controllers)
6. **Add route** in `app/[feature].py`
   - Use `@jwt_required()` for protected endpoints
   - Keep controllers thin - delegate to services
7. **Write tests** in `tests/unit/` and `tests/integration/`
8. **Run tests**: `docker compose exec api pytest`

### Adding a Frontend Feature
1. **Create composable** in `src/composables/use[Feature].ts`
   - Use singleton pattern for global state
   - Export reactive refs and methods
2. **Create component** in `src/components/[Feature]/[Component].vue`
   - Use Composition API `<script setup>`
   - Import composable for state management
3. **Add route** (if new page) in `src/router.ts`
   - Define meta fields for auth requirements
4. **Add i18n translations** in `src/locales/it.json` and `en.json`
5. **Write tests** in `tests/unit/[Feature].spec.ts`
6. **Run tests**: `cd intellyhub-fe && npm run test`

### Creating an FSM Plugin
1. **Create plugin directory**: `ai-automation-fsm-py/intellyhub-plugins/plugins/my-plugin/`
2. **Add manifest.json**:
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "My custom plugin",
     "entry_file": "my_plugin_state.py",
     "type": "state",
     "requirements": ["requests>=2.28.0"]
   }
   ```
3. **Create entry file** `my_plugin_state.py`:
   ```python
   from flow.states.base_state import BaseState

   class MyPluginState(BaseState):
       state_type = "my-plugin"  # REQUIRED for auto-registration

       def execute(self, variables):
           # Your logic here
           return self.success_transition  # or state name
   ```
4. **Optional**: Add `icon.svg` for UI customization
5. **Test**: Run workflow using the plugin
   - Plugin auto-registers via metaclass
   - Requirements auto-install on first use

## Testing Strategy

### Backend Testing (pytest)
```python
# Unit test pattern (tests/unit/)
def test_create_flow_success(client, auth_headers, user):
    """Test flow creation with valid data"""
    data = {'name': 'Test Flow', 'yaml_content': '...'}
    response = client.post('/api/flows', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert 'id' in response.json

# Available fixtures (conftest.py):
# - client: Flask test client
# - auth_headers: JWT authentication headers
# - user: Test user instance
# - db: Database session
```

**Test Organization:**
- `tests/unit/` - Service and utility tests
- `tests/integration/` - API endpoint tests
- `tests/security/` - Auth and authorization tests
- **Coverage target**: ≥80%

**Running Tests:**
```bash
docker compose exec api pytest                 # All tests
docker compose exec api pytest tests/unit/     # Unit only
docker compose exec api pytest --cov=app       # With coverage
```

### Frontend Testing (Vitest + Vue Test Utils)
```typescript
// Component test pattern (tests/unit/)
import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
import MyComponent from '@/components/MyComponent.vue'

describe('MyComponent', () => {
  it('renders properly', () => {
    const wrapper = mount(MyComponent, {
      props: { title: 'Test' }
    })
    expect(wrapper.text()).toContain('Test')
  })

  it('emits event on click', async () => {
    const wrapper = mount(MyComponent)
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted()).toHaveProperty('click')
  })
})
```

**Test Organization:**
- `tests/unit/` - Component tests
- `tests/integration/` - Page/workflow tests
- **Coverage target**: ≥70%

**Running Tests:**
```bash
cd intellyhub-fe
npm run test              # Run tests
npm run test:ui           # Visual test UI
npm run test:coverage     # Coverage report
npm run test:watch        # Watch mode
```

### FSM Engine Testing (pytest)
```bash
cd ai-automation-fsm-py

# Run all tests
pytest

# With coverage
pytest --cov=flow --cov-report=html

# Specific test suites
pytest test/test_states/       # State type tests
pytest test/test_listeners/    # Listener tests
pytest test/test_integration.py -v  # Full flow tests

# Test specific workflow
python main.py test/test_config.yaml
```

**Test Organization:**
- `test/test_states/` - Individual state type tests
- `test/test_listeners/` - Event listener tests
- `test/test_integration.py` - Complete flow execution tests
- `test/test_plugin_loader.py` - Plugin system tests

## Critical Development Gotchas

### Backend
- **ALWAYS use Docker for Flask commands**: `docker compose exec api flask db ...` (NEVER run Flask commands outside Docker)
- **Migrations auto-generated**: Use `flask db migrate` to generate, NEVER create migration files manually
- **Review migrations before applying**: Auto-generated migrations may need adjustments
- **Always use `@jwt_required()`** decorator for protected endpoints
- **Cascade deletes configured**: User deletion removes ALL flows, subscriptions, variables
- **Service layer handles business logic**: Controllers only handle HTTP concerns
- **Use `BaseService`** for automatic audit logging
- **Multi-tenant isolation**: Always filter by `user_id` in queries

### Frontend
- **ALWAYS use relative paths for API calls**: `/api/microservices`, NOT `http://api:5000/api/microservices`
- **axios baseURL must be empty string**: To use Vite proxy (`baseURL: ''`)
- **VITE_API_BASE_URL is for Vite proxy**: Server-side only, must use Docker service name `api`
- **Composables use singleton pattern** for global state (imported multiple times = same instance)
- **Auth token in localStorage**: Key is `token`
- **`useAutomationState` polls every 5 seconds** for flow status (can impact performance)
- **Vue Flow requires exact structure**: Nodes/edges must match Vue Flow API
- **YAML sync uses debounced watcher**: 500ms delay before saving
- **Real-time sync**: YAML editor ↔ visual diagram synchronized

### FSM Engine
- **Plugins loaded lazily**: NOT at startup, only when used in a flow
- **Variable interpolation**: Use `{variable_name}` syntax (recursive)
- **Metaclass auto-registers**: States/listeners auto-register via `StateMeta`/`ListenerMeta`
- **Max steps default: 100**: Prevents infinite loops
- **State execution must return**: Next state name or None for end
- **Listeners must be blocking**: Use `while True` loop
- **Plugin naming**: Entry file must match pattern `{plugin_name}_state.py` or `{plugin_name}_listener.py`

## API Reference

### Key Endpoints

**Authentication:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login (returns JWT token)
- `GET /api/auth/me` - Get current user info

**Flows:**
- `GET /api/flows` - List user's flows
- `POST /api/flows` - Create new flow
- `GET /api/flows/{id}` - Get flow details
- `PUT /api/flows/{id}` - Update flow
- `DELETE /api/flows/{id}` - Delete flow
- `POST /api/flows/{id}/execute` - Execute flow (creates K8s job)
- `GET /api/flows/{id}/status` - Get execution status
- `GET /api/flows/{id}/logs` - Get execution logs

**Versions:**
- `GET /api/flows/{id}/versions` - List flow versions
- `POST /api/flows/{id}/versions/{v}/rollback` - Rollback to version

**Variables & Secrets:**
- `GET /api/variables` - List user variables
- `POST /api/variables` - Create variable
- `DELETE /api/variables/{key}` - Delete variable
- `POST /api/secrets` - Store encrypted secret
- `GET /api/secrets` - List secrets (values not returned)

**Plugins:**
- `POST /api/plugins/repository/sync` - Sync plugin repository
- `POST /api/flows/{id}/plugins/install` - Install plugin for flow
- `GET /api/plugins` - List available plugins

**Billing:**
- `GET /api/billing/plans` - List subscription plans
- `GET /api/billing/subscription` - Current user subscription
- `POST /api/billing/create-checkout-session` - Create Stripe checkout
- `POST /api/billing/webhook` - Stripe webhook handler

**Admin (requires admin role):**
- `GET /api/admin/dashboard` - KPI dashboard
- `GET /api/admin/users` - List all users
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Delete user

**Analytics (admin only):**
- `GET /api/analytics/conversion-rate` - Conversion metrics
- `GET /api/analytics/churn` - Churn rate
- `GET /api/analytics/arpu` - Average revenue per user
- `GET /api/analytics/revenue` - Revenue breakdown

## Troubleshooting

### Testing API Endpoints with Authentication

**Login and get JWT token:**
```bash
# Login with user credentials
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"YourPassword"}'

# Response contains access_token:
# {"access_token":"eyJhbGci...","expires_in":3600,"user":{...}}

# Test protected endpoint with token
curl http://localhost:5000/api/microservices/ \
  -H "Authorization: Bearer eyJhbGci..."

# Expected response: {"microservices":[],"total":0}
```

**Testing in browser console:**
```javascript
// 1. Login and save token
fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({email: 'user@example.com', password: 'YourPassword'})
})
.then(r => r.json())
.then(data => {
  localStorage.setItem('token', data.access_token)
  console.log('Token saved:', data.access_token)
})

// 2. Test API with saved token
fetch('/api/microservices/', {
  headers: {'Authorization': `Bearer ${localStorage.getItem('token')}`}
})
.then(r => r.json())
.then(data => console.log('Microservices:', data))
```

### Frontend Network Errors (ERR_NAME_NOT_RESOLVED)

**Problem:** Browser tries to call `http://api:5000/api/endpoint` directly instead of using Vite proxy.

**Common Causes:**
1. **Browser cache** - Cached JavaScript bundles with old axios configuration
2. **Vite build cache** - Stale optimized dependencies in `node_modules/.vite`
3. **Hard-coded URLs** - Absolute URLs instead of relative paths in code

**Solutions:**

**Option 1: Clear browser cache**
```bash
# Hard refresh in browser:
# - Chrome/Firefox: Ctrl+Shift+F5 (Windows/Linux) or Cmd+Shift+R (Mac)
# - Or open in Incognito/Private mode
# - Or clear browser cache completely
```

**Option 2: Clear Vite cache and rebuild**
```bash
# Stop frontend
docker compose stop frontend

# Clear Vite cache
docker compose exec frontend rm -rf node_modules/.vite

# Rebuild and restart
docker compose up -d --build frontend

# Check logs
docker compose logs frontend --tail 20
```

**Option 3: Full reset (nuclear option)**
```bash
# Stop all services
docker compose down

# Remove volumes (DANGER: deletes database data)
docker compose down -v

# Rebuild everything
docker compose up -d --build

# Reapply migrations
docker compose exec api flask db upgrade
```

**Verification:**
1. Open browser DevTools (F12) → Network tab
2. Navigate to problematic page (e.g., http://localhost:5173/microservices)
3. Check API calls:
   - ✅ **Correct**: Request URL shows `http://localhost:5173/api/microservices` (proxied)
   - ❌ **Wrong**: Request URL shows `http://api:5000/api/microservices` (direct)

**Root Cause Check:**
```bash
# Verify axios configuration in container
docker compose exec frontend cat /app/src/axios.ts
# Should have: baseURL: ''

# Verify composable uses relative paths
docker compose exec frontend grep "axios.get" /app/src/composables/useMicroservices.ts
# Should show: axios.get('/api/microservices')

# Verify Vite proxy config
docker compose exec frontend cat /app/vite.config.ts
# Should have proxy: { '/api': { target: process.env.VITE_API_BASE_URL } }

# Verify environment variable
docker compose exec frontend env | grep VITE
# Should show: VITE_API_BASE_URL=http://api:5000
```

### Port Conflicts
```bash
# Check which process uses port
sudo lsof -i :5000   # Backend
sudo lsof -i :5173   # Frontend
sudo lsof -i :5432   # Database

# Kill process
sudo kill -9 <PID>
```

### Database Issues
```bash
# Check database status
docker compose exec db pg_isready -U user -d intellyhub

# Reset database (DANGER: deletes all data)
docker compose down -v
docker compose up -d
docker compose exec api flask db upgrade
docker compose exec api python populate_plans.py
```

### Plugin Not Loading
1. Check `state_type` class attribute is defined
2. Verify file in correct directory (`flow/states/` or `flow/listeners/`)
3. Check `manifest.json` exists and is valid JSON
4. Review logs for import errors: `docker compose logs api -f`
5. Ensure requirements installed: `python main.py plugins list`

### Frontend Build Errors
```bash
cd intellyhub-fe

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

### Flow Execution Fails
1. Check YAML syntax: `docker compose exec api python3 -c "import yaml; yaml.safe_load(open('flow.yaml'))"`
2. Verify Kubernetes config: `docker compose exec api kubectl get pods`
3. Check FSM executor image exists: `docker images | grep fsm-executor`
4. Review flow logs: `GET /api/flows/{id}/logs`
5. Test flow locally: `cd ai-automation-fsm-py && python main.py flow.yaml --verbose`

## Service URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Docs (Swagger)**: http://localhost:5000/api/docs
- **Database**: localhost:5432 (user: `user`, password: `pass`, database: `intellyhub`)

## Documentation References

- **Backend API**: Swagger UI at http://localhost:5000/api/docs
- **YAML DSL**: `ai-automation-fsm-py/documentazione/YAML_DSL_COMPLETE_GUIDE.md`
- **Plugin System**: `ai-automation-fsm-py/documentazione/PLUGIN_SYSTEM.md`
- **Plugin Creation**: `ai-automation-fsm-py/documentazione/PLUGIN_CREATION_GUIDE.md`
- **Lazy Loading**: `ai-automation-fsm-py/documentazione/LAZY_LOADING_SYSTEM.md`
- **Auto-restart**: `ai-automation-fsm-py/documentazione/AUTO_RESTART_MECHANISM.md`
- **Package Manager**: `ai-automation-fsm-py/documentazione/PACKAGE_MANAGER_DOCUMENTATION.md`
- **Performance Optimization**: `ai-automation-fsm-py/documentazione/PERFORMANCE_OPTIMIZATION.md` ⚡

## Important Reminders

- **Use Docker Compose**: Direct Python/Node execution may have dependency issues
- **Migrations required**: Never modify database directly - always create migrations
- **YAML must be valid**: Follow FSM DSL specification strictly
- **Plugin naming**: No conflicts with built-in state types/listeners
- **Stripe webhooks**: Require HTTPS in production (use Stripe CLI locally via `./stripe-tunnel.sh`)
- **Kubernetes**: Valid KUBECONFIG required for flow execution
- **Submodules**: Remember to commit submodule updates to parent repo
