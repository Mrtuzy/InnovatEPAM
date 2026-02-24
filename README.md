# InnovatEPAM Portal

Innovation idea submission and evaluation portal for EPAM employees.

## Features

- **User Management**: Registration, login, role-based access (submitter/admin)
- **Idea Submission**: Create ideas with title, description, category, and file attachments
- **Idea Evaluation**: Admin workflow for reviewing and evaluating submitted ideas
- **Idea Tracking**: View submitted ideas with status updates and evaluation comments

## Project Structure

```
InnovatEPAM/
├── backend/           # FastAPI backend application
│   ├── src/          # Source code
│   ├── tests/        # Test files
│   └── alembic/      # Database migrations
├── frontend/         # React frontend application
│   ├── src/          # Source code
│   └── tests/        # Test files
└── specs/            # Feature specifications and planning
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Poetry (Python dependency management)
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your database credentials and secret key

5. Run database migrations:
   ```bash
   poetry run alembic upgrade head
   ```

6. Start development server:
   ```bash
   poetry run python src/main.py
   ```

   Backend runs at: http://localhost:8000
   API docs at: http://localhost:8000/api/docs

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file from `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Start development server:
   ```bash
   npm run dev
   ```

   Frontend runs at: http://localhost:3000

## Development

### Running Tests

**Backend:**
```bash
cd backend
poetry run pytest
poetry run pytest --cov=src --cov-report=html
```

**Frontend:**
```bash
cd frontend
npm run test              # Unit tests
npm run test:coverage     # With coverage
npm run test:e2e          # End-to-end tests
```

### Code Quality

**Backend:**
```bash
cd backend
poetry run black .        # Format code
poetry run ruff check .   # Lint code
poetry run mypy src/      # Type checking
```

**Frontend:**
```bash
cd frontend
npm run lint              # Lint code
npm run lint:fix          # Fix linting issues
npm run format            # Format code
npm run format:check      # Check formatting
```

## Architecture

- **Backend**: Python 3.11 + FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite
- **Authentication**: JWT tokens with HTTP-only cookies
- **Testing**: pytest (backend), Vitest (frontend unit), Playwright (frontend e2e)

## Documentation

- **API Documentation**: http://localhost:8000/api/docs (when backend is running)
- **Feature Specifications**: See `specs/001-portal-mvp/` directory
- **Technical Plan**: See `specs/001-portal-mvp/plan.md`
- **Constitution**: See `.specify/memory/constitution.md`

## License

Internal EPAM project - All rights reserved.
