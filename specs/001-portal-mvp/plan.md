# Implementation Plan: InnovatEPAM Portal Phase 1 MVP

**Branch**: `001-portal-mvp` | **Date**: 2026-02-24 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-portal-mvp/spec.md`

**Note**: This document outlines the technical approach for implementing the InnovatEPAM Portal Phase 1 MVP.

## Summary

Build a web-based innovation portal enabling employee idea submission and admin evaluation. Core capabilities include user registration/authentication with role-based access (submitter/admin), idea submission with file attachments, idea listing with role-filtered views, and admin evaluation workflow with status management and feedback comments. System prioritizes security (password hashing, RBAC), clean architecture (separated concerns), RESTful API design, and comprehensive testing (70% unit, 20% integration, 10% e2e).

## Technical Context

**Language/Version**: Python 3.11+ (backend), JavaScript ES2022+/TypeScript (frontend)
**Primary Dependencies**: FastAPI 0.104+ (backend API), SQLAlchemy 2.0+ (ORM), Pydantic 2.0+ (validation), React 18+ with Vite (frontend)
**Storage**: PostgreSQL 14+ (relational data), Local filesystem development / S3-compatible production (file attachments)
**Testing**: pytest + pytest-cov + pytest-asyncio (backend), Vitest + React Testing Library (frontend unit), Playwright (e2e)
**Target Platform**: Web application - modern browsers (Chrome, Firefox, Safari, Edge latest 2 versions), responsive design for desktop/tablet
**Project Type**: Web application (full-stack) - RESTful API backend + SPA frontend
**Performance Goals**: 100 concurrent users, <2s idea list load, <1s authentication, <10s file upload (10MB), <200ms API response p95
**Constraints**: 99% uptime during business hours, 80% code coverage (auth/ideas modules), TDD mandatory, <30 lines per function
**Scale/Scope**: MVP targets ~50-200 active users, ~100 ideas/user max, single deployment environment, manual admin provisioning

**Technology Decisions**: All unknowns resolved in [research.md](research.md). Key choices:
- Python/FastAPI for type-safe, async-capable backend with excellent testing ecosystem
- PostgreSQL for ACID compliance and relational integrity
- React with Vite for component reusability and modern development experience
- JWT with HTTP-only cookies for stateless, secure authentication
- bcrypt for password hashing (12 rounds) per security requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Clean Architecture & Separation of Concerns
✅ **PASS** - Architecture will separate:
- Domain models (User, Idea, Category, Evaluation) - framework-independent
- Services layer (business logic: validation, authorization, workflow rules)
- Repository layer (data access abstraction)
- API controllers (orchestration only, no business logic)
- Clear dependency flow: Controllers → Services → Repositories → Models

### Principle II: RESTful API Design
✅ **PASS** - API design follows REST:
- Resource-based URLs: `/api/v1/users`, `/api/v1/ideas`, `/api/v1/ideas/{id}/evaluations`
- Standard HTTP methods: GET (list/read), POST (create), PUT/PATCH (update), DELETE (remove)
- Proper status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Server Error)
- Stateless design with JWT/session tokens
- API versioning: `/api/v1/` prefix

### Principle III: Test-First Development (NON-NEGOTIABLE)
✅ **PASS** - Testing strategy aligned:
- TDD workflow: Write test → Run (fail) → Implement → Run (pass) → Refactor
- Testing pyramid: 70% unit (models, services, utilities), 20% integration (API endpoints, repository layer), 10% e2e (user journeys)
- Minimum 80% coverage for auth and ideas modules
- Test naming: `test_action_condition_expectedResult`
- All 24 acceptance scenarios from spec will drive test creation

### Principle IV: Code Quality Standards
✅ **PASS** - Quality measures enforced:
- Pre-commit hooks for linting (flake8/black for Python, ESLint/Prettier for frontend)
- Maximum 30 lines per function
- Code review required with automated quality gates
- Single Responsibility Principle in all components
- DRY principle - extract reusable utilities

### Principle V: Security-First Approach
✅ **PASS** - Security built-in:
- Password hashing: bcrypt or Argon2 (NEVER plain text or weak hashing)
- RBAC enforced at service layer with role checks before any protected operation
- Input validation via Pydantic models/schemas on all API endpoints
- SQL injection prevention: ORM with parameterized queries only
- XSS prevention: frontend output encoding, API content-type validation
- File upload validation: size limits (10MB), type restrictions, virus scanning consideration
- HTTPS in production, secure session/JWT handling
- No sensitive data in logs or API responses

**Constitution Compliance**: ✅ ALL GATES PASS - No violations requiring justification

## Project Structure

### Documentation (this feature)

```text
specs/001-portal-mvp/
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions and architecture patterns
├── data-model.md        # Phase 1: Entity definitions and relationships
├── quickstart.md        # Phase 1: Development setup guide
├── contracts/           # Phase 1: API endpoint specifications
│   ├── auth.md         # Authentication endpoints
│   ├── users.md        # User management endpoints
│   ├── ideas.md        # Idea CRUD endpoints
│   └── evaluations.md  # Evaluation workflow endpoints
└── checklists/
    └── requirements.md  # Specification validation checklist
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── user.py          # User entity (email, hashed_password, role)
│   │   ├── idea.py          # Idea entity (title, description, category, status)
│   │   ├── category.py      # Category entity (predefined list)
│   │   └── evaluation.py    # Evaluation entity (admin comment, status change)
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── idea_repository.py
│   │   └── evaluation_repository.py
│   ├── services/
│   │   ├── auth_service.py       # Registration, login, logout, session management
│   │   ├── user_service.py       # User operations, role management
│   │   ├── idea_service.py       # Idea CRUD, validation, file handling
│   │   └── evaluation_service.py # Admin evaluation workflow
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py           # Auth endpoints
│   │   │   ├── users.py          # User endpoints
│   │   │   ├── ideas.py          # Idea endpoints
│   │   │   └── evaluations.py    # Evaluation endpoints
│   │   └── middleware/
│   │       ├── auth_middleware.py    # JWT/session validation
│   │       └── rbac_middleware.py    # Role-based access control
│   ├── schemas/
│   │   ├── user_schemas.py       # Pydantic models for validation
│   │   ├── idea_schemas.py
│   │   └── evaluation_schemas.py
│   ├── utils/
│   │   ├── password_hasher.py    # bcrypt/Argon2 wrapper
│   │   ├── file_handler.py       # File upload/storage utilities
│   │   └── validators.py         # Custom validation logic
│   ├── config/
│   │   └── settings.py           # Configuration management
│   └── main.py                   # Application entry point
└── tests/
    ├── unit/
    │   ├── models/
    │   ├── services/
    │   └── utils/
    ├── integration/
    │   ├── api/
    │   └── repositories/
    └── e2e/
        └── user_journeys/

frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── ideas/
│   │   │   ├── IdeaList.jsx
│   │   │   ├── IdeaDetail.jsx
│   │   │   └── IdeaSubmissionForm.jsx
│   │   └── admin/
│   │       └── EvaluationPanel.jsx
│   ├── pages/
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── IdeasPage.jsx
│   │   └── AdminPage.jsx
│   ├── services/
│   │   ├── authService.js       # API calls for auth
│   │   ├── ideaService.js       # API calls for ideas
│   │   └── evaluationService.js # API calls for evaluations
│   ├── utils/
│   │   ├── apiClient.js         # Axios/fetch wrapper with auth
│   │   └── validators.js        # Frontend validation helpers
│   └── App.jsx                  # Root component with routing
└── tests/
    ├── unit/
    │   └── components/
    └── e2e/
        └── journeys/

uploads/                          # Local file storage (development)
└── ideas/                        # Idea attachments organized by ID

.env.example                      # Environment variables template
.gitignore                        # Exclude .env, uploads/, __pycache__
README.md                         # Project overview and setup
requirements.txt                  # Python dependencies
package.json                      # Node dependencies
docker-compose.yml               # Optional: local development stack
```

**Structure Decision**: Web application architecture selected (Option 2 from template) due to:
- Clear separation between API backend and UI frontend
- Independent scalability and deployment options
- Enables API-first development with contract testing
- Supports future mobile client or third-party integrations
- Aligns with RESTful API design principle from constitution

## Complexity Tracking

> No constitutional violations detected - this section remains empty per template guidance.

---

## Phase Completion Status

✅ **Phase 0 Complete**: [research.md](research.md) - All technology decisions finalized
✅ **Phase 1 Complete**: Design artifacts created:
- [data-model.md](data-model.md) - Entity definitions and relationships
- [contracts/auth.md](contracts/auth.md) - Authentication API endpoints
- [contracts/ideas.md](contracts/ideas.md) - Ideas and evaluation API endpoints
- [quickstart.md](quickstart.md) - Development environment setup

**Constitution Re-Check**: ✅ ALL PRINCIPLES VERIFIED

Architecture aligns with all constitutional principles:
- Clean architecture enforced through layered design (controllers → services → repositories → models)
- RESTful API contracts defined with proper HTTP methods and status codes
- TDD workflow established with testing pyramid (70/20/10 split) and naming conventions
- Code quality standards embedded in tooling (linting, formatting, type checking)
- Security-first approach implemented (bcrypt, RBAC, input validation, file security)

**Next Phase**: **NOT** created by /speckit.plan - Run `/speckit.tasks` to generate [tasks.md](tasks.md) for implementation breakdown

---

**Implementation Plan Status**: ✅ COMPLETE - Ready for task decomposition and development
