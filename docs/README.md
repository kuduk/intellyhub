# IntellyHub Documentation Hub

This directory acts as the single entry point for every piece of documentation in the repository. Each link below points to an existing, actively maintained file.

## 📘 Core Guides (root project)
- [README.md](../README.md) — high-level overview and key capabilities
- [docs/quick-start.md](quick-start.md) — bring the platform online with Docker Compose
- [docs/installation.md](installation.md) — prerequisites, manual/Docker/K8s setup, environment variables
- [docs/architecture.md](architecture.md) — end-to-end overview of frontend, backend, FSM engine, and infrastructure

## 🧰 Backend (Flask API)
- [intellyhub-be/docs/README.md](../intellyhub-be/docs/README.md) — backend index covering:
  - [api-reference.md](../intellyhub-be/docs/api-reference.md)
  - [development-guide.md](../intellyhub-be/docs/development-guide.md)
  - [database.md](../intellyhub-be/docs/database.md)
- Deep dives in `intellyhub-be/documentazione/`:
  - [SECURITY_SYSTEM.md](../intellyhub-be/documentazione/SECURITY_SYSTEM.md) — hardening & controls
  - [BILLING_INTEGRATION.md](../intellyhub-be/documentazione/BILLING_INTEGRATION.md) — Stripe plans & flows
  - [PLUGIN_SYSTEM.md](../intellyhub-be/documentazione/PLUGIN_SYSTEM.md) — backend plugin lifecycle
  - [ADMIN_INVOICE_MANAGEMENT.md](../intellyhub-be/documentazione/ADMIN_INVOICE_MANAGEMENT.md) — admin panel & invoicing
  - [LANGCHAIN_CHAT_SYSTEM.md](../intellyhub-be/documentazione/LANGCHAIN_CHAT_SYSTEM.md) — AI chat integration

## 🖥️ Frontend (Vue 3 + Vuetify)
- [intellyhub-fe/docs/README.md](../intellyhub-fe/docs/README.md) — frontend index
  - [development-guide.md](../intellyhub-fe/docs/development-guide.md)
  - [flow-editor.md](../intellyhub-fe/docs/flow-editor.md)
  - [composables.md](../intellyhub-fe/docs/composables.md)
- For more details, browse `intellyhub-fe/src/` for components/composables/pages and `intellyhub-fe/tests/` for Vitest examples.

## ⚙️ FSM Engine (ai-automation-fsm-py)
- [ai-automation-fsm-py/docs/README.md](../ai-automation-fsm-py/docs/README.md) — engine overview
  - [state-types.md](../ai-automation-fsm-py/docs/state-types.md)
  - [listeners.md](../ai-automation-fsm-py/docs/listeners.md)
- Extended documentation in `ai-automation-fsm-py/documentazione/`:
  - [YAML_DSL_COMPLETE_GUIDE.md](../ai-automation-fsm-py/documentazione/YAML_DSL_COMPLETE_GUIDE.md)
  - [PLUGIN_SYSTEM.md](../ai-automation-fsm-py/documentazione/PLUGIN_SYSTEM.md)
  - [AUTO_RESTART_MECHANISM.md](../ai-automation-fsm-py/documentazione/AUTO_RESTART_MECHANISM.md)
  - [LAZY_LOADING_SYSTEM.md](../ai-automation-fsm-py/documentazione/LAZY_LOADING_SYSTEM.md)
  - [PACKAGE_MANAGER_DOCUMENTATION.md](../ai-automation-fsm-py/documentazione/PACKAGE_MANAGER_DOCUMENTATION.md)

## 🧪 Testing & Operations
- [TESTING_GUIDE.md](../TESTING_GUIDE.md) — cross-project testing strategies
- [MICROSERVICES_FEATURE_COMPLETE.md](../MICROSERVICES_FEATURE_COMPLETE.md) — microservice requirements & status
- [PLUGIN_ICONS_GUIDE.md](../PLUGIN_ICONS_GUIDE.md) — branding rules for plugin icons
- [QUICKSTART_OPTIMIZATION.md](../QUICKSTART_OPTIMIZATION.md) — performance tuning notes

## How to Use This Index
1. Start from the **Core Guides** to set up the platform and understand the architecture.
2. Jump to the area you need (Backend, Frontend, FSM Engine) and open the corresponding module README.
3. Consult the `documentazione/` folders when you need in-depth details about specific features or fixes.

Documentation is maintained for **IntellyHub v2.0**. If you discover inconsistencies, please open an issue and include the file path plus commit.
