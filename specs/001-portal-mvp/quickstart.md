# Quick Start Guide: InnovatEPAM Portal Phase 1 MVP

**Purpose**: Get the development environment running in < 15 minutes  
**Last Updated**: 2026-02-24

---

## Prerequisites

### Required Software
- **Python**: 3.11 or higher ([python.org](https://python.org))
- **Node.js**: 18 or higher ([nodejs.org](https://nodejs.org))
- **PostgreSQL**: 14 or higher ([postgresql.org](https://postgresql.org))
- **Git**: Latest version

### Optional but Recommended
- **Docker Desktop**: For containerized development environment
- **VS Code**: With Python and ESLint extensions
- **Postman** or **Insomnia**: For API testing

---

## Quick Start (Docker - Recommended)

### 1. Clone and Setup

```bash
# Clone repository
git clone <repository-url>
cd InnovatEPAM

# Copy environment template
cp .env.example .env

# Edit .env with your settings (most defaults work for local dev)
```

### 2. Start Services

```bash
# Start all services (PostgreSQL + Backend + Frontend)
docker-compose up -d

# View logs
docker-compose logs -f backend
```

### 3. Initialize Database

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Seed initial data (categories, test admin account)
docker-compose exec backend python -m src.scripts.seed_data
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **API Redoc**: http://localhost:8000/redoc

### 5. Test Accounts

After seeding:
- **Admin**: admin@innovatepam.com / Admin123!
- **Submitter**: submitter@innovatepam.com / Submit123!

---

## Manual Setup (Without Docker)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb innovatepam_dev

# Update .env with database connection
# DATABASE_URL=postgresql://postgres:password@localhost:5432/innovatepam_dev

# Run migrations
alembic upgrade head

# Seed initial data
python -m src.scripts.seed_data
```

### 3. Start Backend Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Backend now running at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 4. Frontend Setup

Open a **new terminal** (keep backend running):

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.example .env

# Update .env with backend API URL
# VITE_API_URL=http://localhost:8000/api/v1
```

### 5. Start Frontend Server

```bash
# Development mode with HMR
npm run dev

# Frontend now running at http://localhost:3000
```

---

## Environment Configuration

### Backend (.env)

```bash
# Application
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-change-this-in-production
API_VERSION=v1

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/innovatepam_dev

# Authentication
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
PASSWORD_BCRYPT_ROUNDS=12

# File Upload
MAX_FILE_SIZE_MB=10
UPLOAD_DIR=./uploads
ALLOWED_FILE_TYPES=pdf,doc,docx,xls,xlsx,jpg,jpeg,png,gif

# CORS (for frontend)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Optional: Email (for future phases)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASSWORD=
```

### Frontend (.env)

```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api/v1

# Application
VITE_APP_NAME=InnovatEPAM Portal
VITE_MAX_FILE_SIZE_MB=10
```

---

## Verify Installation

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

### 2. Check API Documentation

Visit: http://localhost:8000/docs

You should see Swagger UI with all endpoints listed.

### 3. Test Authentication

```bash
# Register a test user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPass123!"
  }'
```

### 4. Check Frontend

Visit: http://localhost:3000

You should see the login page.

---

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# Run specific test file
pytest tests/unit/services/test_auth_service.py

# Run tests matching pattern
pytest -k "test_login"

# View coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run unit tests with coverage
npm run test:coverage

# Run e2e tests (requires backend running)
npm run test:e2e

# Run e2e tests in UI mode
npm run test:e2e:ui
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b 001-portal-mvp
```

### 2. Make Changes Following TDD

```bash
# Example: Adding a new service method

# 1. Write test first (RED)
# Edit: tests/unit/services/test_idea_service.py
pytest tests/unit/services/test_idea_service.py::test_create_idea_validData_returnsCreatedIdea
# Test should FAIL

# 2. Implement feature (GREEN)
# Edit: src/services/idea_service.py
pytest tests/unit/services/test_idea_service.py::test_create_idea_validData_returnsCreatedIdea
# Test should PASS

# 3. Refactor if needed
# Clean up code, run tests again to ensure still passing
```

### 3. Run Linters

```bash
# Backend
cd backend
black src/  # Format code
flake8 src/ # Check style
mypy src/   # Type checking

# Frontend
cd frontend
npm run lint       # ESLint
npm run format     # Prettier
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: implement idea creation endpoint

- Add IdeaService.create_idea method
- Add POST /api/v1/ideas endpoint
- Add file upload handling
- Add tests with 85% coverage
"
```

### 5. Pre-commit Hooks (Recommended)

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Now linting runs automatically on git commit
```

---

## Database Migrations

### Create New Migration

```bash
cd backend

# Auto-generate migration from model changes
alembic revision --autogenerate -m "add evaluation table"

# Edit the generated file in alembic/versions/ if needed

# Apply migration
alembic upgrade head
```

### Useful Migration Commands

```bash
# View current migration version
alembic current

# View migration history
alembic history

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Upgrade to specific version
alembic upgrade <revision_id>
```

---

## Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Activate virtual environment and install dependencies
```bash
cd backend
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**: Start PostgreSQL and verify DATABASE_URL in .env
```bash
# Check if PostgreSQL is running
pg_isready

# Start PostgreSQL (varies by OS)
# Windows: Start PostgreSQL service from Services
# macOS: brew services start postgresql
# Linux: sudo systemctl start postgresql
```

---

### Frontend won't start

**Error**: `Cannot find module 'react'`

**Solution**: Install dependencies
```bash
cd frontend
npm install
```

---

**Error**: `Failed to fetch from API`

**Solution**: Verify backend is running and VITE_API_URL is correct
```bash
# Check backend health
curl http://localhost:8000/health

# Verify .env file
cat frontend/.env
# Should show: VITE_API_URL=http://localhost:8000/api/v1
```

---

### Tests failing

**Error**: Test database connection issues

**Solution**: Create separate test database
```bash
createdb innovatepam_test

# Update tests/conftest.py or set env variable
export TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/innovatepam_test
```

---

### File uploads not working

**Error**: `Permission denied: uploads/`

**Solution**: Create uploads directory and set permissions
```bash
cd backend
mkdir uploads
chmod 755 uploads

# Or set UPLOAD_DIR in .env to a writable location
```

---

### Docker issues

**Error**: `Cannot connect to Docker daemon`

**Solution**: Start Docker Desktop

---

**Error**: Port already in use

**Solution**: Stop conflicting services or change ports in docker-compose.yml
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

---

## Useful Commands Cheat Sheet

### Backend
```bash
# Start development server
uvicorn src.main:app --reload

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src/

# Run linter
flake8 src/

# Type check
mypy src/

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Seed database
python -m src.scripts.seed_data
```

### Frontend
```bash
# Start development server
npm run dev

# Run tests
npm test

# Run e2e tests
npm run test:e2e

# Lint code
npm run lint

# Format code
npm run format

# Build for production
npm run build
```

### Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Execute command in container
docker-compose exec backend bash
```

---

## Next Steps

1. **Read Documentation**:
   - [plan.md](plan.md) - Technical architecture
   - [data-model.md](data-model.md) - Database entities
   - [contracts/](contracts/) - API specifications

2. **Review Constitution**:
   - [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
   - Understand TDD requirements, code quality standards, security principles

3. **Start Development**:
   - Pick a user story from [spec.md](spec.md)
   - Write tests first (TDD)
   - Implement feature
   - Run tests and linters
   - Submit PR

4. **Join Team Communication**:
   - Ask questions in team chat
   - Review existing PRs to understand patterns
   - Pair program with team members

---

## Getting Help

- **Documentation**: Check `specs/001-portal-mvp/` directory
- **API Reference**: http://localhost:8000/docs (when backend running)
- **Constitution**: `.specify/memory/constitution.md` (coding standards)
- **Issues**: Check existing GitHub issues or create new one
- **Code Examples**: Review `tests/` directories for usage patterns

---

**Quick Start Complete!** You should now have a running development environment. Proceed to implementing user stories following TDD principles from the constitution.
