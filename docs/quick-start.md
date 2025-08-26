# Quick Start Guide

Get IntellyHub running on your system in under 10 minutes.

## Prerequisites

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Git**: For cloning the repository

Check your versions:
```bash
docker --version          # Should be >= 20.10
docker compose --version  # Should be >= 2.0
```

## 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/kuduk/IntellyHub.git
cd IntellyHub

# Setup environment for backend (creates .env from template)
cd intellyhub-be
cp .env.example .env
# Edit .env with your configurations (optional for quick start)
cd ..
```

## 2. Start All Services

The docker-compose.yml in the root directory orchestrates all services:

```bash
# Start all services (API + Frontend + Database)
docker compose up -d --build

# Verify services are running
docker compose ps

# View logs if needed
docker compose logs -f api
docker compose logs -f frontend
```

## 3. Initialize Database

```bash
# Database migrations are applied automatically via entrypoint.sh
# But you can run them manually if needed:
docker compose exec api flask db upgrade

# Create sample billing plans
docker compose exec api python3 populate_plans.py

# Create admin user (follow the interactive prompts)
docker compose exec api python3 setup_admin.py
```

## 4. Access the Application

- **Frontend**: http://localhost:5173 (Vue 3 + Vite + Vuetify)
- **Backend API**: http://localhost:5000/docs (Flask with Swagger UI in development)
- **Database**: localhost:5432 (PostgreSQL - user: user, password: pass, database: intellyhub)

## 5. Test the System

1. **Open the frontend** at http://localhost:5173
2. **Register a new user** or login with the admin account you created
3. **Create your first automation flow**:
   - Click "Create Flow"
   - Use the visual editor to add states
   - Save and execute your flow

## Next Steps

- Read the [User Guide](user-guide.md) to learn about creating automations
- Check the [Plugin Reference](plugin-reference.md) for available integrations
- See [Configuration Guide](configuration.md) for advanced setup
- Visit [Developer Guide](developer-guide.md) if you want to contribute

## Troubleshooting Quick Issues

### Services Won't Start
```bash
# Check logs
docker compose logs api
docker compose logs frontend
```

### Database Connection Issues
```bash
# Wait for database to be ready
docker compose exec db pg_isready -U user -d intellyhub
```

### Port Conflicts
If ports 5173 or 5000 are in use, modify `docker-compose.yml` to use different ports.

### Reset Everything
```bash
# Stop all services and remove volumes
docker compose down -v

# Restart fresh
docker compose up -d --build
```

## What's Running

After successful startup:

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 5173 | Vue.js user interface |
| Backend API | 5000 | Flask REST API |
| Database | 5432 | PostgreSQL database |

Your IntellyHub installation is now ready! 🚀