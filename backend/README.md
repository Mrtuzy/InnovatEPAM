# InnovatEPAM Backend

FastAPI backend for InnovatEPAM Portal.

## Tech Stack

- **Framework**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **Validation**: Pydantic 2.0+
- **Database**: PostgreSQL 14+
- **Authentication**: JWT tokens with bcrypt password hashing
- **Testing**: pytest with coverage
- **Code Quality**: Black, Ruff, MyPy

## Project Structure

```
backend/
├── src/
│   ├── api/              # API endpoints
│   │   ├── middleware/   # Auth, RBAC, error handling
│   │   └── v1/          # API v1 routes
│   ├── config/          # Configuration and database setup
│   ├── models/          # SQLAlchemy models
│   ├── repositories/    # Data access layer
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── utils/           # Utilities (JWT, password hashing, logging)
│   └── main.py          # Application entry point
├── tests/
│   ├── unit/            # Unit tests (70%)
│   ├── integration/     # Integration tests (20%)
│   └── e2e/            # End-to-end tests (10%)
├── alembic/             # Database migrations
│   └── versions/        # Migration files
├── pyproject.toml       # Dependencies and configuration
└── alembic.ini          # Alembic configuration
```

## Setup

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Create `.env` file**:
   ```bash
   cp .env.example .env
   ```

4. **Configure environment variables** in `.env`:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: JWT secret (generate with `openssl rand -hex 32`)

5. **Run migrations**:
   ```bash
   poetry run alembic upgrade head
   ```

6. **Start server**:
   ```bash
   poetry run python src/main.py
   ```

## Development

### Running Tests

```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=src --cov-report=html

# Specific test file
poetry run pytest tests/unit/test_auth.py

# Watch mode
poetry run pytest-watch
```

### Code Quality

```bash
# Format code
poetry run black src/ tests/

# Lint
poetry run ruff check src/ tests/

# Fix linting issues
poetry run ruff check --fix src/ tests/

# Type checking
poetry run mypy src/
```

### Database Migrations

```bash
# Create new migration
poetry run alembic revision --autogenerate -m "description"

# Apply migrations
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# View migration history
poetry run alembic history
```

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## Testing Strategy

Following the project constitution:
- **70% Unit Tests**: Test individual functions and classes
- **20% Integration Tests**: Test API endpoints with database
- **10% E2E Tests**: Test complete user journeys

Minimum 80% coverage required for `auth` and `ideas` modules.

## Authentication

- JWT access tokens (15-minute expiry)
- JWT refresh tokens (7-day expiry, HTTP-only cookie)
- bcrypt password hashing (12 rounds)
- Role-based access control (submitter/admin)

## Environment Variables

See `.env.example` for all available configuration options.
