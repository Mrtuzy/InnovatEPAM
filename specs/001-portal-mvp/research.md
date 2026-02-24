# Research & Technology Decisions: InnovatEPAM Portal Phase 1 MVP

**Purpose**: Resolve technical unknowns from plan.md Technical Context and establish technology choices  
**Date**: 2026-02-24  
**Status**: Complete

## Research Questions from Technical Context

This document resolves all "NEEDS CLARIFICATION" items identified in the Technical Context section of plan.md.

---

## 1. Backend Language & Framework Selection

### Decision
**Python 3.11+ with FastAPI**

### Rationale
- **Type Safety**: Python 3.11+ with type hints + Pydantic provides strong compile-time validation aligning with constitution's quality standards
- **Performance**: FastAPI built on Starlette (async/await) handles 100+ concurrent users requirement efficiently
- **Developer Experience**: Automatic OpenAPI/Swagger documentation generation supports API-first development
- **Testing Ecosystem**: pytest provides excellent TDD support with fixtures, parametrization, and coverage tools
- **Security Libraries**: Mature passlib (bcrypt/Argon2), python-jose (JWT), python-multipart (file uploads)
- **Clean Architecture Support**: FastAPI's dependency injection system enables clean separation of concerns
- **Community & Stability**: Large ecosystem, active development, production-proven (used by Microsoft, Uber, Netflix)

### Alternatives Considered
- **Node.js/Express**: Excellent but JavaScript's looser typing increases testing burden for 80% coverage goal
- **Django REST Framework**: More opinionated, includes unwanted features (admin panel), heavier for API-only backend
- **Go/Gin**: Superior performance but smaller ecosystem, longer development time for MVP

---

## 2. Primary Backend Dependencies

### Decision
**Core Stack**:
- **FastAPI 0.104+**: Web framework and API routing
- **SQLAlchemy 2.0+**: ORM for database abstraction (supports clean architecture repository pattern)
- **Alembic**: Database migrations
- **Pydantic 2.0+**: Data validation and serialization
- **passlib + bcrypt**: Password hashing (bcrypt algorithm per constitution)
- **python-jose**: JWT token handling for stateless authentication
- **python-multipart**: File upload handling
- **httpx**: Async HTTP client for testing

**Testing**:
- **pytest**: Test runner and fixtures
- **pytest-cov**: Coverage reporting (80% threshold enforcement)
- **pytest-asyncio**: Async test support
- **faker**: Test data generation

**Quality**:
- **black**: Code formatting (automated)
- **flake8**: Linting (pre-commit enforcement)
- **mypy**: Static type checking

### Rationale
- All choices aligned with constitutional principles (security, quality, testing)
- SQLAlchemy's repository pattern support enables clean architecture
- Pydantic validates all inputs at API boundary (security principle)
- pytest ecosystem provides complete TDD support (test-first principle)

---

## 3. Frontend Framework Selection

### Decision
**React 18+ with Vite**

### Rationale
- **Component Reusability**: Aligns with DRY principle from constitution
- **Strong Typing Option**: TypeScript support for quality standards
- **Testing Ecosystem**: Jest/Vitest + React Testing Library for unit tests, Playwright for e2e
- **Developer Experience**: Vite provides fast HMR, excellent development workflow
- **Industry Standard**: Largest ecosystem, easiest to hire for, most documentation
- **State Management**: Built-in hooks sufficient for MVP scope; Redux/Zustand available if needed

### Frontend Dependencies
**Core**:
- **React 18+**: UI framework
- **React Router v6**: Client-side routing
- **Axios**: HTTP client with interceptors (authentication headers)
- **React Hook Form**: Form validation and state management
- **TanStack Query**: Server state management and caching

**UI/UX**:
- **Tailwind CSS** or **Material-UI**: Component styling (Tailwind recommended for customization)
- **React Icons**: Icon library

**Testing**:
- **Vitest**: Fast unit test runner (Jest-compatible API)
- **React Testing Library**: Component testing following best practices
- **Playwright**: E2e testing for user journeys

**Quality**:
- **ESLint**: JavaScript/React linting
- **Prettier**: Code formatting
- **TypeScript** (optional but recommended): Static typing for better quality

### Alternatives Considered
- **Vue 3**: Excellent but smaller ecosystem, less ubiquitous
- **Angular**: Too heavy for MVP, opinionated framework increases complexity
- **Svelte**: Excellent performance but smaller ecosystem, riskier for team scaling

---

## 4. Database & Storage Selection

### Decision
**PostgreSQL 14+ for relational data + Local filesystem (development) / S3-compatible (production) for file attachments**

### Rationale

**PostgreSQL Choice**:
- **Relational Model Fit**: User, Idea, Evaluation entities have clear relationships requiring referential integrity
- **JSON Support**: Flexible for future schema evolution (idea metadata, category configuration)
- **Full-Text Search**: Native support if search feature added in future phases
- **ACID Compliance**: Critical for evaluation workflow consistency (prevents lost status updates)
- **Performance**: Handles 100 concurrent users easily with proper indexing
- **SQLAlchemy Support**: First-class ORM integration
- **Open Source**: No licensing costs, wide deployment options

**File Storage Strategy**:
- **Development**: Local filesystem (`uploads/` directory)
  - Simple setup, no external dependencies
  - Git-ignored for security
- **Production**: S3-compatible object storage (AWS S3, MinIO, Backblaze B2)
  - Scalable, durable (11 9's for S3)
  - Separate file storage from application servers enables horizontal scaling
  - Pre-signed URLs for secure direct uploads
  - Automatic backups and versioning

### Alternatives Considered
- **MySQL**: Good but PostgreSQL's JSON support and full-text search future-proof the choice
- **SQLite**: Insufficient for concurrent write requirements (idea submissions + evaluations)
- **MongoDB**: Overkill for structured data, loses referential integrity benefits
- **Blob storage in database**: Degrades database performance, complicates backups

---

## 5. Testing Framework & Strategy

### Decision
**Backend**: pytest + pytest-cov + pytest-asyncio  
**Frontend**: Vitest + React Testing Library + Playwright  
**Coverage**: 80% minimum for auth and ideas modules (enforced via CI)

### Testing Pyramid Implementation

**Unit Tests (70% of test suite)**:
- **Backend**: 
  - Service layer business logic (auth, idea validation, evaluation rules)
  - Utility functions (password hashing, file validation, validators)
  - Model methods (entity behavior)
- **Frontend**: 
  - React components (isolated rendering, user interactions)
  - Service functions (API call logic, error handling)
  - Utility functions (validators, formatters)

**Integration Tests (20% of test suite)**:
- **Backend**: 
  - API endpoints (request → response flow through all layers)
  - Repository layer (database interactions)
  - Middleware (authentication, RBAC enforcement)
- **Frontend**: 
  - Component integration (forms with validation, page flows)
  - API service integration with mock servers

**E2E Tests (10% of test suite)**:
- **Full User Journeys** (Playwright):
  - User registration → login → idea submission → view list
  - Admin login → view all ideas → accept/reject with comment
  - Session expiration and re-authentication
  - File attachment upload and download

### Test Naming Convention
Following constitution requirement: `test_action_condition_expectedResult`

Examples:
- `test_register_validData_createsUserWithSubmitterRole`
- `test_login_invalidPassword_returns401Unauthorized`
- `test_submitIdea_unauthenticatedUser_returns403Forbidden`
- `test_evaluateIdea_nonAdminUser_returns403Forbidden`
- `test_uploadFile_exceedsLimit_returns400BadRequest`

---

## 6. Additional Technology Decisions

### Authentication Strategy
**Decision**: JWT tokens with HTTP-only cookies

**Rationale**:
- Stateless (aligns with RESTful principle II)
- HTTP-only cookies prevent XSS attacks (security principle V)
- Refresh token rotation for enhanced security
- Simple logout (clear cookie)

**Implementation**:
- Access token: Short-lived (15 minutes), contains user ID and role
- Refresh token: Longer-lived (7 days), used to obtain new access token
- Token validation middleware on all protected routes

### API Versioning
**Decision**: URL path versioning (`/api/v1/`)

**Rationale**:
- Explicit and discoverable
- Simple routing in FastAPI
- Allows future breaking changes without disrupting existing clients

### Development Tools
**Decision**:
- **Docker Compose**: Local development stack (PostgreSQL + backend + frontend)
- **Pre-commit hooks**: Automated linting and formatting before commits
- **GitHub Actions** (or similar CI/CD): Automated tests, coverage checks, deployment

### File Upload Security
**Decision**: Multi-layer validation

**Implementation**:
- Size limit: 10MB (enforced at API middleware)
- Type validation: File extension + MIME type checking
- Filename sanitization: Remove special characters, prevent path traversal
- Virus scanning: Integration with ClamAV or similar (optional for MVP, recommended for production)
- Storage isolation: Uploaded files stored outside web root, served via secure endpoints

---

## Best Practices from Research

### RESTful API Design Patterns

**Resource Naming**:
```
POST   /api/v1/auth/register        # User registration
POST   /api/v1/auth/login           # User login
POST   /api/v1/auth/logout          # User logout
GET    /api/v1/users/{id}           # Get user profile
GET    /api/v1/ideas                # List ideas (filtered by role)
POST   /api/v1/ideas                # Create idea
GET    /api/v1/ideas/{id}           # Get idea detail
POST   /api/v1/ideas/{id}/evaluate  # Admin evaluate idea (status + comment)
```

**Status Code Usage**:
- 200: Successful GET/PUT/PATCH
- 201: Successful POST (resource created)
- 400: Validation error (bad input)
- 401: Authentication required (not logged in)
- 403: Authorization failed (logged in but wrong role)
- 404: Resource not found
- 500: Server error

### Clean Architecture Layers

**Dependency Flow**: Controllers → Services → Repositories → Models

```
API Controller (FastAPI route handler)
    ↓ calls
Service Layer (business logic, validation, authorization)
    ↓ calls
Repository Layer (data access abstraction)
    ↓ uses
SQLAlchemy Models (database entities)
```

**Benefits**:
- Business logic testable without database (mock repositories)
- Controllers remain thin (orchestration only, no business logic)
- Easy to swap data sources (SQL → NoSQL) by changing repository

### Password Security Pattern
```python
# Using passlib with bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing (registration)
hashed_password = pwd_context.hash(plain_password)

# Verification (login)
is_valid = pwd_context.verify(plain_password, hashed_password)
```

**Configuration**: bcrypt rounds = 12 (balance between security and performance)

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Backend Language** | Python | 3.11+ | Application logic, API |
| **Backend Framework** | FastAPI | 0.104+ | REST API, routing, validation |
| **Database** | PostgreSQL | 14+ | Relational data storage |
| **ORM** | SQLAlchemy | 2.0+ | Database abstraction |
| **Validation** | Pydantic | 2.0+ | Request/response schemas |
| **Password Hashing** | passlib + bcrypt | Latest | Secure password storage |
| **Authentication** | python-jose (JWT) | Latest | Stateless auth tokens |
| **File Handling** | python-multipart | Latest | File upload support |
| **Frontend Framework** | React | 18+ | UI components |
| **Build Tool** | Vite | 5+ | Fast development, bundling |
| **HTTP Client** | Axios | 1.6+ | API communication |
| **Styling** | Tailwind CSS | 3+ | Utility-first styling |
| **Backend Testing** | pytest | 7+ | Test runner, fixtures |
| **Frontend Testing** | Vitest | 1+ | Unit/integration tests |
| **E2E Testing** | Playwright | 1.40+ | User journey tests |
| **Linting (Python)** | flake8 + black | Latest | Code quality |
| **Linting (JS)** | ESLint + Prettier | Latest | Code quality |
| **Local Dev** | Docker Compose | Latest | Development stack |

---

## Implementation Sequence Recommendation

Based on constitutional principle III (Test-First Development) and user story priorities (P1 → P4):

1. **Foundation** (Phase 1):
   - Database schema and migrations
   - Authentication infrastructure (JWT, password hashing)
   - Base models and repositories
   - API structure and middleware

2. **User Story P1 Implementation** (Auth):
   - User registration (TDD: tests → implementation)
   - Login/logout (TDD)
   - Role assignment
   - Session management

3. **User Story P2 Implementation** (Idea Submission):
   - Idea creation endpoint (TDD)
   - File upload handling (TDD)
   - Validation rules (TDD)

4. **User Story P3 Implementation** (Idea Listing):
   - List endpoints with role filtering (TDD)
   - Detail view endpoint (TDD)

5. **User Story P4 Implementation** (Admin Evaluation):
   - Evaluation endpoint (TDD)
   - Status workflow (TDD)
   - Comment handling (TDD)

Each story independently testable and deliverable per specification requirements.

---

**Status**: All NEEDS CLARIFICATION items resolved. Proceed to Phase 1 (Data Model & Contracts).
