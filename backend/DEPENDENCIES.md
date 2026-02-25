# Backend Dependency Management

## Overview

This project supports two dependency management approaches:

1. **Poetry** (Modern, Recommended) - Uses `pyproject.toml`
2. **pip** (Traditional) - Uses `requirements.txt`

## For Development

### Using Poetry

```powershell
# Install Poetry (if not already installed)
pip install poetry

# Install dependencies
cd backend
poetry install

# Add new dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Run commands in Poetry environment
poetry run pytest
poetry run uvicorn src.main:app --reload
```

### Using pip + requirements.txt

```powershell
# Install dependencies
cd backend
pip install -r requirements.txt

# Install in editable mode for development
pip install -e .
```

## Updating requirements.txt from Poetry

If you add dependencies via Poetry and need to update `requirements.txt`:

```powershell
cd backend

# Export production dependencies
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Or export with dev dependencies
poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev
```

## Current Dependencies

### Production
- **fastapi** ^0.104.0 - Web framework
- **uvicorn** ^0.24.0 - ASGI server
- **sqlalchemy** ^2.0.0 - ORM
- **alembic** ^1.12.0 - Database migrations
- **psycopg2-binary** ^2.9.9 - PostgreSQL adapter
- **pydantic** ^2.0.0 - Data validation
- **pydantic-settings** ^2.0.0 - Settings management
- **bcrypt** ^4.1.0 - Password hashing
- **python-jose[cryptography]** ^3.3.0 - JWT tokens
- **python-multipart** ^0.0.6 - File uploads
- **email-validator** ^2.1.0 - Email validation
- **python-dotenv** ^1.0.0 - Environment variables

### Development
- **pytest** ^7.4.0 - Testing framework
- **pytest-cov** ^4.1.0 - Coverage reporting
- **pytest-asyncio** ^0.21.0 - Async test support
- **httpx** ^0.25.0 - HTTP client for tests
- **ruff** ^0.1.0 - Fast linter
- **black** ^23.11.0 - Code formatter
- **mypy** ^1.7.0 - Type checking
- **faker** ^20.0.0 - Test data generation

## Which One Should You Use?

### Use Poetry if:
- You're starting fresh development
- You want better dependency resolution
- You prefer modern Python tooling
- You need lockfile support (poetry.lock)

### Use pip + requirements.txt if:
- You're deploying to restricted environments
- You prefer simple, traditional approach
- Your CI/CD doesn't support Poetry
- You're using Docker (can be simpler)

## CI/CD Considerations

For production deployments, `requirements.txt` is often simpler:

**Dockerfile example:**
```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

**With Poetry:**
```dockerfile
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev --no-root
```

Both approaches work well - choose based on your deployment infrastructure.
