# Installation Guide

This guide covers all installation methods for IntellyHub, from development setup to production deployment.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Development Setup](#development-setup)
- [Production Installation](#production-installation)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Required Software

| Component | Minimum Version | Recommended Version |
|-----------|-----------------|-------------------|
| Docker | 20.10 | Latest stable |
| Docker Compose | 2.0 | Latest stable |
| Git | 2.0 | Latest stable |
| Node.js | 16.x | 18.x (for manual frontend setup) |
| Python | 3.9 | 3.11 (for manual backend setup) |

### System Requirements

**Development Environment**:
- RAM: 8GB minimum, 32GB recommended
- Disk: 10GB free space
- CPU: 4 cores minimum

**Production Environment**:
- RAM: 32GB minimum, 64GB+ recommended
- Disk: 50GB+ free space
- CPU: 16+ cores recommended
- Network: Stable internet connection

### Verify Prerequisites

```bash
# Check Docker
docker --version
docker compose --version

# Check Git
git --version

# Check system resources
docker system df  # Check Docker disk usage
docker system info | grep Memory  # Check available memory
```

## Development Setup

### Option 1: Full Docker Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/kuduk/IntellyHub.git
cd IntellyHub

# 2. Configure environment
cd intellyhub-be
cp .env.example .env
# Edit .env file with your settings (see Environment Configuration below)
cd ..

# 3. Start all services
docker compose up -d --build

# 4. Initialize database
docker compose exec api python3 -m flask db upgrade
docker compose exec api python3 populate_plans.py
docker compose exec api python3 setup_admin.py

# 5. Verify installation
curl http://localhost:5000/health
curl http://localhost:5173
```

### Option 2: Manual Setup

#### Backend Setup
```bash
cd intellyhub-be

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your database URL and other settings

# Initialize database
flask db upgrade

# Create admin user
python setup_admin.py

# Start development server
python run.py
```

#### Frontend Setup
```bash
cd intellyhub-fe

# Install dependencies
npm install

# Start development server
npm run dev
```

#### FSM Engine Setup
```bash
cd ai-automation-fsm-py

# Install dependencies
pip install -r requirements.txt

# Test installation
python -m pytest test/
```

## Production Installation

### Docker Swarm Deployment

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

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=intellyhub
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  flows_data:
  db_data:
```

Deploy with:
```bash
docker stack deploy -c docker-stack.yml intellyhub
```

### Kubernetes Deployment

```yaml
# k8s-namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: intellyhub

---
# k8s-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: intellyhub-config
  namespace: intellyhub
data:
  FLASK_ENV: "production"
  DATABASE_URL: "postgresql+psycopg2://user:pass@postgres:5432/intellyhub"

---
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intellyhub-api
  namespace: intellyhub
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
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

Apply with:
```bash
kubectl apply -f k8s-namespace.yaml
kubectl apply -f k8s-configmap.yaml
kubectl apply -f k8s-deployment.yaml
```

## Environment Configuration

### Backend Environment Variables (.env)

```bash
# === CORE CONFIGURATION ===
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development  # or production
DEBUG=True  # False for production

# === DATABASE ===
DATABASE_URL=postgresql+psycopg2://user:pass@db:5432/intellyhub

# === REDIS (OPTIONAL) ===
REDIS_URL=redis://localhost:6379/0

# === STRIPE BILLING ===
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
STRIPE_PRICE_ID_STANDARD=price_standard_plan_id
STRIPE_PRICE_ID_BUSINESS=price_business_plan_id
STRIPE_PRICE_ID_ENTERPRISE=price_enterprise_plan_id

# === AI SERVICES ===
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_ASSISTANT_ID=asst_your_assistant_id

# === KUBERNETES ===
KUBE_CONFIG_PATH=/path/to/kubeconfig
K8S_NAMESPACE=intellyhub-production
FSM_EXECUTOR_IMAGE=fsm-executor:latest

# === EMAIL ===
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=True

# === SECURITY ===
BCRYPT_ROUNDS=12
JWT_ACCESS_TOKEN_EXPIRES_HOURS=4
JWT_ADMIN_TOKEN_EXPIRES_HOURS=1

# === MONITORING ===
PROMETHEUS_METRICS=true
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project-id
```

### Frontend Environment Variables (.env)

```bash
# API Configuration
VITE_API_URL=http://localhost:5000
VITE_API_TIMEOUT=30000

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_CHAT=true
VITE_ENABLE_BILLING=true

# External Services
VITE_STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key

# Build Configuration
VITE_BUILD_VERSION=2.0.0
VITE_BUILD_ENV=development
```

## Database Setup

### PostgreSQL Configuration

#### Using Docker (Recommended for Development)
```bash
# Database is automatically configured in docker-compose.yml
# Default credentials:
# - Database: intellyhub
# - User: user
# - Password: pass
# - Port: 5432
```

#### Manual PostgreSQL Setup
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib  # Ubuntu
brew install postgresql  # macOS

# Start PostgreSQL service
sudo systemctl start postgresql  # Ubuntu
brew services start postgresql  # macOS

# Create database and user
sudo -u postgres psql
CREATE DATABASE intellyhub;
CREATE USER intellyhub_user WITH ENCRYPTED PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE intellyhub TO intellyhub_user;
\q
```

### Database Migrations

```bash
# Apply all migrations
docker compose exec api flask db upgrade

# Or manually
cd intellyhub-be
flask db upgrade

# Create new migration (for development)
flask db migrate -m "Description of changes"
```

### Database Backup and Restore

```bash
# Create backup
docker compose exec db pg_dump -U user intellyhub > backup.sql

# Restore backup
docker compose exec -T db psql -U user intellyhub < backup.sql
```

## Service Verification

### Health Checks

```bash
# Backend API health
curl http://localhost:5000/health

# Database connection
docker compose exec api python -c "from app import create_app; app = create_app(); print('Database connection: OK')"

# Frontend availability
curl http://localhost:5173
```

### Service Logs

```bash
# View all service logs
docker compose logs -f

# View specific service logs
docker compose logs -f api
docker compose logs -f frontend
docker compose logs -f db
```

## Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using the ports
sudo lsof -i :5000  # Backend port
sudo lsof -i :5173  # Frontend port
sudo lsof -i :5432  # Database port

# Kill processes if needed
sudo kill -9 <PID>
```

#### Docker Issues
```bash
# Clean up Docker
docker compose down -v  # Stop and remove volumes
docker system prune -f  # Remove unused resources

# Rebuild containers
docker compose build --no-cache
docker compose up -d
```

#### Database Connection Issues
```bash
# Check database status
docker compose exec db pg_isready -U user -d intellyhub

# Check database logs
docker compose logs db

# Reset database
docker compose down -v
docker compose up -d db
# Wait for db to be ready, then restart other services
docker compose up -d
```

#### Permission Issues
```bash
# Fix Docker permissions (Linux)
sudo usermod -aG docker $USER
# Log out and back in

# Fix file permissions
chmod +x intellyhub-be/entrypoint.sh
```

### Getting Help

If you encounter issues:
1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Review service logs with `docker compose logs`
3. Check [GitHub Issues](https://github.com/kuduk/IntellyHub/issues)
4. Ensure all prerequisites are met

## Next Steps

After successful installation:
- Follow the [Quick Start Guide](quick-start.md) to create your first automation
- Read the [Configuration Guide](configuration.md) for advanced setup
- Check the [Security Guide](security.md) for production hardening