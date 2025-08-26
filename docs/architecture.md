# IntellyHub Architecture

IntellyHub is a modern, cloud-native automation platform built with microservices architecture and containerized deployment.

## System Overview

Based on the actual docker-compose.yml and code structure:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   Vue 3 + Vite │◄──►│  Flask + SQLAlch│◄──►│  PostgreSQL 15  │
│   Port: 5173    │    │   Port: 5000    │    │   Port: 5432    │
│   (Vuetify UI)  │    │  (REST API)     │    │  (Primary DB)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         │              ┌─────────────────┐              │
         │              │   Kubernetes    │              │
         │              │ Flow Execution  │              │
         │              │  (fsm-executor  │              │
         │              │   containers)   │              │
         │              └─────────────────┘              │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ FSM Engine      │
                    │ (ai-automation- │
                    │    fsm-py)      │
                    │ - States        │
                    │ - Listeners     │
                    │ - Plugins       │
                    └─────────────────┘
```

## Core Components

### 1. Frontend (intellyhub-fe)
**Technology**: Vue 3 + TypeScript + Vuetify + Vite

**Real Implementation Features**:
- Vue Flow visual editor (`AutomationDesignView.vue`)
- Composables-based state management (`useAuth`, `useFlows`, `usePlugins`)
- Real-time automation status polling (`useAutomationState`)
- Admin panel with role-based permissions (`usePermissions`)
- Multi-language support via vue-i18n
- Theme switching with Vuetify

**Verified Components**:
- `Navbar.vue` - Main navigation
- `AutomationDesignView.vue` - Flow editor with Vue Flow
- Node components: `StartNode`, `EndNode`, `IfNode`, `LoopNode`, `CommandNode`, `PluginStateNode`
- Pages: Dashboard, AutomationEdit, Store, Profile, Login, Register

### 2. Backend API (intellyhub-be)
**Technology**: Flask + SQLAlchemy + PostgreSQL

**Real Implementation**: Service layer pattern with Flask blueprints

**Verified Blueprints** (from app/__init__.py):
- `/api/auth` - Authentication (JWT-based)
- `/api/flows` - Flow management and execution
- `/health` - Health checks and system status
- `/` - API documentation (Swagger UI in development)
- `/api/variables` - User variable management
- `/api/secrets` - Encrypted secret storage
- `/api/chat` - AI chat functionality
- `/api/plugins` - Plugin management
- `/api/billing` - Stripe billing integration
- `/api/analytics` - Business analytics
- `/api/exports` - Data export functionality
- `/api/notifications` - Notification system
- `/api/admin` - Admin panel operations
- `/api/audit` - Audit logging

**Real Service Layer**:
- `BaseService` - Abstract base with logging and audit
- `FlowService` - Flow creation, execution, version management
- Additional services for modular business logic

### 3. FSM Engine (ai-automation-fsm-py)
**Technology**: Python 3.11 + Finite State Machine + Lazy Loading

**Real Implementation** (verified from main.py and flow/):

**Core Architecture**:
- `main.py` - Entry point with plugin manager and auto-restart
- `flow/flow.py` - `FlowDiagram` class and `create_state()` factory
- `STATE_REGISTRY` - Dynamic state registration via metaclasses
- `LISTENER_REGISTRY` - Dynamic listener registration via metaclasses

**Verified State Types** (from flow/states/):
- `CommandState` - Shell commands, HTTP, MQTT, email, eval
- `IfState` - Conditional branching
- `LoopState` - Iteration and repetition  
- `EndState` - Flow termination
- `LlmAgentState` - AI/LLM integration
- `TelegramBotState` - Telegram messaging
- `FacebookState`, `LinkedinState`, `WechatState` - Social integrations
- `RssReaderState` - RSS feed processing
- `FileState` - File operations
- `SwitchState` - Multi-way branching
- `McpState`, `TextToSpeechState` - Additional integrations

**Verified Listeners** (from flow/listeners/):
- `EmailListener`, `WebhookListener`, `RssListener`
- `TelegramListener`, `DirectoryListener`, `MqttListener`, `McpListener`
- All use `ListenerMeta` metaclass for auto-registration

### 4. Database Layer
**Technology**: PostgreSQL 15

**Responsibilities**:
- User and organization data
- Flow definitions and versions
- Execution history and logs
- Billing and subscription data
- Plugin configurations
- Audit trail storage

**Key Features**:
- ACID transactions
- Advanced indexing for performance
- Regular automated backups
- Connection pooling

## Data Flow Architecture

### 1. Flow Creation
```
User Interface → Backend API → Database
              ↓
         Plugin Analysis
              ↓
    Auto-suggestion System
```

### 2. Flow Execution
```
API Request → Flow Service → Kubernetes Job
                          ↓
                    FSM Executor Container
                          ↓
                   Plugin State Execution
                          ↓
                     Results Storage
```

### 3. Real-time Updates
```
FSM Executor → Kubernetes Logs → Backend Streaming → Frontend Updates
```

## Security Architecture

### Multi-Layer Security
1. **Network Layer**: HTTPS/TLS encryption
2. **Application Layer**: JWT authentication, RBAC authorization
3. **Data Layer**: Encrypted sensitive data, audit logging
4. **Infrastructure Layer**: Container isolation, Kubernetes security

### Authentication Flow
```
Client → JWT Token → Backend Validation → Resource Access
   ↓
Role-based Permissions Check
   ↓
Audit Log Entry
```

## Scalability Design

### Horizontal Scaling
- **Frontend**: CDN distribution, multiple replicas
- **Backend**: Load balancer with multiple API instances
- **Database**: Read replicas, connection pooling
- **Execution**: Kubernetes auto-scaling for flow jobs

### Performance Optimization
- **Caching**: Redis for session and frequently accessed data
- **Database**: Query optimization, proper indexing
- **CDN**: Static asset distribution
- **Compression**: Gzip/Brotli for API responses

## Plugin Architecture

### Plugin System
```
Core Engine ← Plugin Loader ← Plugin Repository
     ↓             ↓              ↓
State Registry  Manifest    GitHub Repository
                Validation   (intellyhub-plugins)
```

### Plugin Types
1. **State Plugins**: Custom workflow states
2. **Listener Plugins**: External event sources
3. **Integration Plugins**: Third-party service connectors

## Deployment Architecture

### Development Environment
```
Docker Compose
├── Frontend Container (Vite dev server)
├── Backend Container (Flask dev server)
├── Database Container (PostgreSQL)
└── Shared Volumes for hot-reload
```

### Production Environment
```
Kubernetes Cluster
├── Frontend Deployment (Nginx + Static files)
├── Backend Deployment (Gunicorn + Flask)
├── Database StatefulSet (PostgreSQL with persistent volumes)
├── Redis Deployment (Caching layer)
└── Flow Execution Jobs (Dynamic FSM containers)
```

## Integration Points

### External Services
- **Stripe**: Payment processing and billing
- **OpenAI**: AI/LLM integrations
- **Email Providers**: SMTP for notifications
- **Cloud Storage**: File storage and backups
- **Monitoring**: Prometheus metrics, logging

### API Integrations
- **RESTful APIs**: Standard HTTP/JSON communication
- **WebHooks**: Real-time event notifications
- **WebSockets**: Live updates and chat functionality
- **GraphQL**: Planned for complex queries

## Development Architecture

### Service Layer Pattern
```
Controllers (HTTP) → Services (Business Logic) → Models (Data Access)
                              ↓
                        Utilities & Helpers
```

### Testing Strategy
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **End-to-End Tests**: Full workflow testing
- **Performance Tests**: Load and stress testing

## Monitoring and Observability

### Metrics Collection
- **Application Metrics**: Prometheus integration
- **Business Metrics**: User activity, flow executions
- **System Metrics**: Resource usage, performance
- **Security Metrics**: Authentication, authorization events

### Logging Strategy
- **Structured Logging**: JSON format with correlation IDs
- **Centralized Logs**: ELK stack or similar
- **Audit Trails**: Comprehensive security logging
- **Error Tracking**: Sentry integration

This architecture provides a robust, scalable, and maintainable platform for enterprise automation needs.