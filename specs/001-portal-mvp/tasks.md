# Tasks: InnovatEPAM Portal Phase 1 MVP

**Input**: Design documents from `/specs/001-portal-mvp/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)

**Tests**: This project follows TDD approach per constitution requirements (70% unit, 20% integration, 10% e2e). Test tasks are included and MUST be written first.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This is a web application with:
- Backend: `backend/src/` for source, `backend/tests/` for tests
- Frontend: `frontend/src/` for source, `frontend/tests/` for tests

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend project structure with src/ and tests/ directories per plan.md
- [X] T002 Initialize Python project with pyproject.toml, configure Poetry/pip with FastAPI 0.104+, SQLAlchemy 2.0+, Pydantic 2.0+, pytest, bcrypt
- [X] T003 [P] Initialize frontend project with Vite 5+, React 18+, configure package.json with TypeScript, Vitest, Playwright
- [X] T004 [P] Configure linting (Ruff/pylint for backend, ESLint for frontend) and formatting (Black for backend, Prettier for frontend)
- [X] T005 Setup PostgreSQL 14+ connection in backend/src/config/settings.py with environment variable support
- [X] T006 Create database initialization script with Alembic for migrations in backend/alembic/
- [X] T007 Configure pytest with coverage settings in backend/pyproject.toml targeting 80% minimum for auth and ideas modules
- [X] T008 [P] Configure Vitest for frontend unit tests in frontend/vitest.config.ts
- [X] T009 [P] Configure Playwright for e2e tests in frontend/playwright.config.ts

**Checkpoint**: Project structure initialized, dependencies installed, test frameworks configured

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Create base database models in backend/src/models/base.py with UUID primary key, created_at, updated_at fields
- [X] T011 Setup database session management in backend/src/config/database.py with connection pooling
- [X] T012 Create base repository pattern in backend/src/repositories/base_repository.py with CRUD operations
- [X] T013 Implement password hasher utility in backend/src/utils/password_hasher.py using bcrypt with 12 rounds
- [X] T014 Create JWT token utility in backend/src/utils/jwt_handler.py with token generation/validation (15-minute access, 7-day refresh)
- [X] T015 Implement authentication middleware in backend/src/api/middleware/auth_middleware.py for JWT validation
- [X] T016 Implement RBAC middleware in backend/src/api/middleware/rbac_middleware.py for role checking (submitter/admin)
- [X] T017 Create Pydantic base schemas in backend/src/schemas/base_schemas.py with common response models
- [X] T018 Setup error handling middleware in backend/src/api/middleware/error_handler.py with standardized error responses
- [X] T019 Configure logging in backend/src/utils/logger.py with structured logging (no sensitive data)
- [X] T020 Create FastAPI application entry point in backend/src/main.py with CORS, middleware registration, API router mounting
- [X] T021 Create API v1 router structure in backend/src/api/v1/__init__.py
- [X] T022 [P] Setup frontend API client in frontend/src/api/client.ts with axios, authentication header injection, error handling
- [X] T023 [P] Create frontend routing structure in frontend/src/routes.tsx with React Router
- [X] T024 [P] Create authentication context in frontend/src/contexts/AuthContext.tsx for user state management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts, log in securely, and access the portal with role-based permissions (submitter/admin)

**Independent Test**: Register a new user account, log in with credentials, verify role assignment in response, access /auth/me endpoint, log out, verify session termination

### Tests for User Story 1 (TDD - Write First)

**Unit Tests (70%)**

- [X] T025 [P] [US1] Unit test for User model validation in backend/tests/unit/models/test_user.py (email format, password hashing, role enum)
- [X] T026 [P] [US1] Unit test for password_hasher utility in backend/tests/unit/utils/test_password_hasher.py (hash generation, verification)
- [X] T027 [P] [US1] Unit test for JWT handler utility in backend/tests/unit/utils/test_jwt_handler.py (token creation, validation, expiration)
- [X] T028 [P] [US1] Unit test for UserRepository CRUD operations in backend/tests/unit/repositories/test_user_repository.py (create, get by email, unique constraint)
- [X] T029 [P] [US1] Unit test for AuthService registration logic in backend/tests/unit/services/test_auth_service_register.py (validation, duplicate email, password requirements)
- [X] T030 [P] [US1] Unit test for AuthService login logic in backend/tests/unit/services/test_auth_service_login.py (valid credentials, invalid credentials, generic error message)
- [X] T031 [P] [US1] Unit test for auth middleware in backend/tests/unit/middleware/test_auth_middleware.py (valid token, expired token, missing token)

**Integration Tests (20%)**

- [X] T032 [US1] Integration test for POST /auth/register endpoint in backend/tests/integration/api/test_auth_register.py (successful registration, duplicate email 409, validation errors 400)
- [X] T033 [US1] Integration test for POST /auth/login endpoint in backend/tests/integration/api/test_auth_login.py (valid credentials, invalid credentials, token response structure)
- [X] T034 [US1] Integration test for POST /auth/logout endpoint in backend/tests/integration/api/test_auth_logout.py (session termination, cookie clearing)
- [X] T035 [US1] Integration test for POST /auth/refresh endpoint in backend/tests/integration/api/test_auth_refresh.py (valid refresh token, expired token)
- [X] T036 [US1] Integration test for GET /auth/me endpoint in backend/tests/integration/api/test_auth_me.py (authenticated request, unauthenticated 401)

**E2E Tests (10%)**

- [X] T037 [US1] E2E test for complete registration and login flow in frontend/tests/e2e/auth/test_registration_login.spec.ts (Playwright: register → verify redirect → login → see dashboard)

### Implementation for User Story 1

**Backend Models**

- [X] T038 [US1] Create User model in backend/src/models/user.py (id UUID PK, email unique, hashed_password, full_name, role enum, is_active, timestamps)
- [X] T039 [US1] Create Alembic migration for User table in backend/alembic/versions/001_create_users_table.py (with indexes on email, role)

**Backend Repositories**

- [X] T040 [US1] Implement UserRepository in backend/src/repositories/user_repository.py (create_user, get_by_email, get_by_id, email case-insensitive lookup)

**Backend Schemas**

- [X] T041 [P] [US1] Create user request schemas in backend/src/schemas/user_schemas.py (RegisterRequest with email/password/full_name validation, LoginRequest)
- [X] T042 [P] [US1] Create user response schemas in backend/src/schemas/user_schemas.py (UserResponse excluding password, TokenResponse with access_token/refresh_token/user)

**Backend Services**

- [X] T043 [US1] Implement AuthService in backend/src/services/auth_service.py (register_user with validation and duplicate check, authenticate_user with password verification, create_tokens, revoke_refresh_token)

**Backend API Endpoints**

- [X] T044 [US1] Implement POST /api/v1/auth/register endpoint in backend/src/api/v1/auth.py (calls AuthService, returns 201 with user data)
- [X] T045 [US1] Implement POST /api/v1/auth/login endpoint in backend/src/api/v1/auth.py (calls AuthService, sets HTTP-only refresh cookie, returns access token)
- [X] T046 [US1] Implement POST /api/v1/auth/logout endpoint in backend/src/api/v1/auth.py (clears refresh token cookie, returns 204)
- [X] T047 [US1] Implement POST /api/v1/auth/refresh endpoint in backend/src/api/v1/auth.py (validates refresh token, issues new access token)
- [X] T048 [US1] Implement GET /api/v1/auth/me endpoint in backend/src/api/v1/auth.py (requires auth middleware, returns current user profile)
- [X] T049 [US1] Register auth router in backend/src/api/v1/__init__.py

**Frontend Components**

- [X] T050 [P] [US1] Create registration form component in frontend/src/components/auth/RegistrationForm.tsx (email, password, full_name inputs with validation)
- [X] T051 [P] [US1] Create login form component in frontend/src/components/auth/LoginForm.tsx (email, password inputs, handles authentication)
- [X] T052 [US1] Create registration page in frontend/src/pages/auth/RegisterPage.tsx (uses RegistrationForm, redirects on success)
- [X] T053 [US1] Create login page in frontend/src/pages/auth/LoginPage.tsx (uses LoginForm, stores token, updates AuthContext)
- [X] T054 [US1] Implement logout functionality in frontend/src/hooks/useAuth.ts (calls logout endpoint, clears auth context, redirects)
- [X] T055 [US1] Create protected route component in frontend/src/components/routing/ProtectedRoute.tsx (checks authentication, redirects if not logged in)
- [X] T056 [US1] Add authentication routes to frontend/src/routes.tsx (/register, /login, /logout)

**Testing Validation**

- [X] T057 [US1] Run all US1 unit tests and verify 70% coverage for auth module in backend/tests/unit/
- [X] T058 [US1] Run all US1 integration tests and verify API contract compliance in backend/tests/integration/
- [X] T059 [US1] Run US1 e2e test and verify complete user journey in frontend/tests/e2e/

**Checkpoint**: User Story 1 complete - users can register, login, logout, and access protected routes with role-based context

---

## Phase 4: User Story 2 - Idea Submission by Users (Priority: P2)

**Goal**: Enable authenticated submitters to create and submit innovation ideas with title, description, category, and optional file attachment

**Independent Test**: Log in as submitter, create an idea with all required fields and a PDF attachment, verify idea appears with "submitted" status and attachment download link

### Tests for User Story 2 (TDD - Write First)

**Unit Tests (70%)**

- [X] T060 [P] [US2] Unit test for Category model in backend/tests/unit/models/test_category.py (name uniqueness, display_order, is_active)
- [X] T061 [P] [US2] Unit test for Idea model validation in backend/tests/unit/models/test_idea.py (title length, description length, status enum, attachment fields consistency)
- [X] T062 [P] [US2] Unit test for file handler utility in backend/tests/unit/utils/test_file_handler.py (file type validation, size validation, filename sanitization, path traversal prevention)
- [X] T063 [P] [US2] Unit test for IdeaRepository in backend/tests/unit/repositories/test_idea_repository.py (create with attachment, foreign key constraints)
- [X] T064 [P] [US2] Unit test for CategoryRepository in backend/tests/unit/repositories/test_category_repository.py (get active categories, get by id)
- [X] T065 [P] [US2] Unit test for IdeaService create logic in backend/tests/unit/services/test_idea_service_create.py (validation, category existence check, file upload handling, submitter association)

**Integration Tests (20%)**

- [X] T066 [US2] Integration test for POST /api/v1/ideas endpoint in backend/tests/integration/api/test_ideas_create.py (successful creation with attachment, without attachment, invalid category 404, file too large 413, unsupported file type 415, validation errors 400, unauthenticated 401)
- [X] T067 [US2] Integration test for GET /api/v1/categories endpoint in backend/tests/integration/api/test_categories.py (returns active categories sorted by display_order)

**E2E Tests (10%)**

- [X] T068 [US2] E2E test for idea submission flow in frontend/tests/e2e/ideas/test_idea_submission.spec.ts (Playwright: login → navigate to submit form → fill fields → attach file → submit → verify success message)

### Implementation for User Story 2

**Backend Models**

- [X] T069 [P] [US2] Create Category model in backend/src/models/category.py (id UUID PK, name unique, description, display_order, is_active, timestamps)
- [X] T070 [US2] Create Idea model in backend/src/models/idea.py (id UUID PK, title, description, category_id FK, submitter_id FK, status enum, attachment fields, timestamps)
- [X] T071 [US2] Create Alembic migration for Category table in backend/alembic/versions/002_create_categories_table.py with seed data for 6 categories
- [X] T072 [US2] Create Alembic migration for Idea table in backend/alembic/versions/003_create_ideas_table.py (with indexes on category_id, submitter_id, status, created_at)

**Backend Utils**

- [X] T073 [US2] Implement file handler utility in backend/src/utils/file_handler.py (validate_file_type, validate_file_size, sanitize_filename, save_file, generate_storage_path, MAX_FILE_SIZE=10MB)

**Backend Repositories**

- [X] T074 [P] [US2] Implement CategoryRepository in backend/src/repositories/category_repository.py (get_active_categories, get_by_id)
- [X] T075 [US2] Implement IdeaRepository in backend/src/repositories/idea_repository.py (create with attachment metadata, get_by_id, get_by_submitter)

**Backend Schemas**

- [X] T076 [P] [US2] Create category schemas in backend/src/schemas/category_schemas.py (CategoryResponse with id/name/description)
- [X] T077 [P] [US2] Create idea request schemas in backend/src/schemas/idea_schemas.py (IdeaCreateRequest with title/description/category_id validation)
- [X] T078 [P] [US2] Create idea response schemas in backend/src/schemas/idea_schemas.py (IdeaResponse with nested category, submitter, attachment details)

**Backend Services**

- [X] T079 [US2] Implement IdeaService in backend/src/services/idea_service.py (create_idea with category validation, file processing, submitter association, status initialization to "submitted")

**Backend API Endpoints**

- [X] T080 [US2] Implement POST /api/v1/ideas endpoint in backend/src/api/v1/ideas.py (multipart/form-data, requires auth, calls IdeaService, returns 201)
- [X] T081 [US2] Implement GET /api/v1/categories endpoint in backend/src/api/v1/categories.py (public or authenticated, returns active categories)
- [X] T082 [US2] Register ideas and categories routers in backend/src/api/v1/__init__.py

**Frontend Components**

- [X] T083 [P] [US2] Create idea submission form component in frontend/src/components/ideas/IdeaSubmissionForm.tsx (title, description, category dropdown, file upload with validation)
- [X] T084 [P] [US2] Create category selector component in frontend/src/components/ideas/CategorySelector.tsx (fetches categories from API, dropdown)
- [X] T085 [P] [US2] Create file upload component in frontend/src/components/ideas/FileUpload.tsx (drag-drop, size/type validation, preview)
- [X] T086 [US2] Create idea submission page in frontend/src/pages/ideas/SubmitIdeaPage.tsx (uses IdeaSubmissionForm, protected route for submitters/admins)
- [X] T087 [US2] Add idea submission route to frontend/src/routes.tsx (/ideas/submit)

**Testing Validation**

- [X] T088 [US2] Run all US2 unit tests and verify coverage for ideas module in backend/tests/unit/
- [X] T089 [US2] Run all US2 integration tests and verify API contract compliance in backend/tests/integration/
- [X] T090 [US2] Run US2 e2e test and verify complete submission journey in frontend/tests/e2e/

**Checkpoint**: User Story 2 complete - submitters can create ideas with attachments, categories are available, ideas stored with "submitted" status

---

## Phase 5: User Story 3 - Idea List and Viewing (Priority: P3)

**Goal**: Enable users to view submitted ideas (submitters see their own, admins see all) with pagination, filtering, and detailed view including attachments

**Independent Test**: Log in as submitter, submit multiple ideas, verify they appear in list with correct metadata; log in as admin, verify all users' ideas visible; click on an idea to see full details including attachment download

### Tests for User Story 3 (TDD - Write First)

**Unit Tests (70%)**

- [X] T091 [P] [US3] Unit test for IdeaRepository list queries in backend/tests/unit/repositories/test_idea_repository_list.py (get_by_submitter with pagination, get_all with pagination, filtering by status/category, sorting)
- [X] T092 [P] [US3] Unit test for IdeaService list logic in backend/tests/unit/services/test_idea_service_list.py (RBAC filtering: submitter sees only own ideas, admin sees all, pagination calculation)
- [X] T093 [P] [US3] Unit test for IdeaService detail logic in backend/tests/unit/services/test_idea_service_detail.py (get by id with authorization check: submitter can view own, admin can view any, other users get 403)

**Integration Tests (20%)**

- [X] T094 [US3] Integration test for GET /api/v1/ideas endpoint in backend/tests/integration/api/test_ideas_list.py (submitter sees only own ideas, admin sees all, pagination headers, status filter, category filter, sorting, unauthenticated 401)
- [X] T095 [US3] Integration test for GET /api/v1/ideas/{id} endpoint in backend/tests/integration/api/test_ideas_detail.py (submitter views own idea, admin views any idea, submitter cannot view other's idea 403, invalid ID 404)
- [X] T096 [US3] Integration test for GET /api/v1/ideas/{id}/attachment endpoint in backend/tests/integration/api/test_ideas_attachment.py (authorized download returns file, unauthorized 403, non-existent attachment 404)

**E2E Tests (10%)**

- [X] T097 [US3] E2E test for idea listing and viewing flow in frontend/tests/e2e/ideas/test_idea_list_view.spec.ts (Playwright: login as submitter → see ideas list → click idea → view details → download attachment)

### Implementation for User Story 3

**Backend Repository Extensions**

- [X] T098 [US3] Extend IdeaRepository in backend/src/repositories/idea_repository.py (get_by_submitter_paginated, get_all_paginated, apply_filters for status/category, apply_sorting)

**Backend Services Extensions**

- [X] T099 [US3] Extend IdeaService in backend/src/services/idea_service.py (list_ideas with RBAC filtering and pagination, get_idea_detail with ownership verification, get_attachment_file with authorization)

**Backend Schemas Extensions**

- [X] T100 [P] [US3] Extend idea schemas in backend/src/schemas/idea_schemas.py (IdeaListResponse with pagination metadata, IdeaSummary for list view with limited fields)

**Backend API Endpoints**

- [X] T101 [US3] Implement GET /api/v1/ideas endpoint in backend/src/api/v1/ideas.py (query params: status, category_id, page, limit, sort; requires auth; returns paginated list)
- [X] T102 [US3] Implement GET /api/v1/ideas/{id} endpoint in backend/src/api/v1/ideas.py (requires auth, RBAC check, returns full idea details)
- [X] T103 [US3] Implement GET /api/v1/ideas/{id}/attachment endpoint in backend/src/api/v1/ideas.py (requires auth, RBAC check, returns file with appropriate MIME type)

**Frontend Components**

- [X] T104 [P] [US3] Create idea list component in frontend/src/components/ideas/IdeaList.tsx (displays ideas table/grid with title, status, category, date, pagination controls)
- [X] T105 [P] [US3] Create idea card component in frontend/src/components/ideas/IdeaCard.tsx (summary view for list display)
- [X] T106 [P] [US3] Create idea detail component in frontend/src/components/ideas/IdeaDetail.tsx (full idea view with description, category, status, attachment download button, evaluation history)
- [X] T107 [P] [US3] Create pagination component in frontend/src/components/common/Pagination.tsx (reusable pagination controls)
- [X] T108 [P] [US3] Create filter component in frontend/src/components/ideas/IdeaFilters.tsx (status filter, category filter, sort dropdown)
- [X] T109 [US3] Create ideas list page in frontend/src/pages/ideas/IdeasListPage.tsx (uses IdeaList, IdeaFilters, protected route)
- [X] T110 [US3] Create idea detail page in frontend/src/pages/ideas/IdeaDetailPage.tsx (uses IdeaDetail, protected route, fetches by ID from URL param)
- [X] T111 [US3] Add idea viewing routes to frontend/src/routes.tsx (/ideas, /ideas/:id)

**Testing Validation**

- [X] T112 [US3] Run all US3 unit tests and verify coverage for list/detail operations in backend/tests/unit/
- [X] T113 [US3] Run all US3 integration tests and verify API contract compliance in backend/tests/integration/
- [X] T114 [US3] Run US3 e2e test and verify complete viewing journey in frontend/tests/e2e/

**Checkpoint**: User Story 3 complete - users can view idea lists (filtered by role), view details, download attachments with proper authorization

---

## Phase 6: User Story 4 - Admin Evaluation Workflow (Priority: P4)

**Goal**: Enable admins to review submitted ideas and make accept/reject/under_review decisions with mandatory feedback comments

**Independent Test**: Log in as admin, view submitted ideas list, select an idea, change status to "under_review", then "accepted" with a comment; verify submitter can see status change and comment when viewing their idea

### Tests for User Story 4 (TDD - Write First)

**Unit Tests (70%)**

- [X] T115 [P] [US4] Unit test for Evaluation model in backend/tests/unit/models/test_evaluation.py (idea_id FK, evaluator_id FK, status transition validation, comment requirement)
- [X] T116 [P] [US4] Unit test for EvaluationRepository in backend/tests/unit/repositories/test_evaluation_repository.py (create evaluation, get evaluations by idea)
- [X] T117 [P] [US4] Unit test for IdeaService evaluation logic in backend/tests/unit/services/test_idea_service_evaluate.py (admin-only check, status transition validation, comment requirement, previous status verification, create evaluation record)

**Integration Tests (20%)**

- [X] T118 [US4] Integration test for POST /api/v1/ideas/{id}/evaluate endpoint in backend/tests/integration/api/test_ideas_evaluate.py (admin accepts with comment, admin rejects with comment, admin sets under_review, non-admin forbidden 403, invalid status transition 400, missing comment 400)
- [X] T119 [US4] Integration test for GET /api/v1/ideas/{id}/evaluations endpoint in backend/tests/integration/api/test_ideas_evaluations.py (returns evaluation history ordered by created_at desc, admin and submitter can view)

**E2E Tests (10%)**

- [X] T120 [US4] E2E test for admin evaluation flow in frontend/tests/e2e/admin/test_evaluation.spec.ts (Playwright: login as admin → view ideas list → click idea → evaluate with comment → verify status change → logout → login as submitter → verify comment visible)

### Implementation for User Story 4

**Backend Models**

- [X] T121 [US4] Create Evaluation model in backend/src/models/evaluation.py (id UUID PK, idea_id FK, evaluator_id FK, previous_status, new_status, comment, created_at)
- [X] T122 [US4] Create Alembic migration for Evaluation table in backend/alembic/versions/004_create_evaluations_table.py (with indexes on idea_id, evaluator_id, created_at)

**Backend Repositories**

- [X] T123 [US4] Implement EvaluationRepository in backend/src/repositories/evaluation_repository.py (create_evaluation, get_evaluations_by_idea)

**Backend Schemas**

- [X] T124 [P] [US4] Create evaluation request schemas in backend/src/schemas/evaluation_schemas.py (EvaluateRequest with new_status enum and comment validation)
- [X] T125 [P] [US4] Create evaluation response schemas in backend/src/schemas/evaluation_schemas.py (EvaluationResponse with evaluator info, previous/new status, comment, timestamp)

**Backend Services Extensions**

- [X] T126 [US4] Extend IdeaService in backend/src/services/idea_service.py (evaluate_idea with admin role check, status transition validation, comment requirement, create evaluation record, update idea status)

**Backend API Endpoints**

- [X] T127 [US4] Implement POST /api/v1/ideas/{id}/evaluate endpoint in backend/src/api/v1/ideas.py (requires auth, admin-only RBAC middleware, calls IdeaService.evaluate_idea)
- [X] T128 [US4] Implement GET /api/v1/ideas/{id}/evaluations endpoint in backend/src/api/v1/ideas.py (requires auth, returns evaluation history for idea)

**Frontend Components**

- [X] T129 [P] [US4] Create evaluation form component in frontend/src/components/admin/EvaluationForm.tsx (status selector: under_review/accepted/rejected, comment textarea, submit button)
- [X] T130 [P] [US4] Create evaluation history component in frontend/src/components/ideas/EvaluationHistory.tsx (displays evaluation timeline with evaluator, status changes, comments)
- [X] T131 [US4] Create admin evaluation page in frontend/src/pages/admin/EvaluateIdeaPage.tsx (protected route admin-only, uses IdeaDetail and EvaluationForm)
- [X] T132 [US4] Extend idea detail page in frontend/src/pages/ideas/IdeaDetailPage.tsx to show EvaluationHistory for all users
- [X] T133 [US4] Add admin evaluation route to frontend/src/routes.tsx (/admin/ideas/:id/evaluate)

**Testing Validation**

- [X] T134 [US4] Run all US4 unit tests and verify coverage for evaluation module in backend/tests/unit/
- [X] T135 [US4] Run all US4 integration tests and verify API contract compliance in backend/tests/integration/
- [X] T136 [US4] Run US4 e2e test and verify complete evaluation journey in frontend/tests/e2e/

**Checkpoint**: User Story 4 complete - admins can evaluate ideas with status changes and comments, evaluation history visible to submitters

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality assurance

- [X] T137 [P] Add API documentation with Swagger/OpenAPI in backend/src/main.py (auto-generated from FastAPI endpoints)
- [X] T138 [P] Create README.md in repository root with project overview, quickstart instructions reference
- [X] T139 [P] Add comprehensive logging for audit trail in backend/src/services/ (user actions, evaluations, errors)
- [X] T140 [P] Implement rate limiting per contracts/auth.md in backend/src/api/middleware/rate_limiter.py (3 registrations/hour, 5 logins/15min)
- [X] T141 Code review and refactoring: ensure all functions <30 lines per constitution
- [X] T142 Security hardening: HTTPS redirect configuration, secure cookie settings, CORS policy review
- [X] T143 Performance optimization: database query optimization, add appropriate indexes review
- [X] T144 [P] Frontend accessibility audit and improvements (ARIA labels, keyboard navigation, screen reader support)
- [X] T145 [P] Frontend responsive design verification (mobile, tablet, desktop breakpoints)
- [X] T146 Run full test suite and verify coverage targets (70% unit, 20% integration, 10% e2e, minimum 80% for auth/ideas modules)
- [X] T147 Validate all endpoints against contracts/auth.md and contracts/ideas.md
- [X] T148 Execute quickstart.md setup guide to verify documentation accuracy
- [X] T149 Create deployment configuration (Docker Compose for development, deployment guide for production)
- [X] T150 Final integration test: complete user journey from registration → idea submission → admin evaluation → submitter viewing feedback

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Setup completion - BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Foundational completion - Must complete before other stories (authentication required for all features)
- **Phase 4 (US2)**: Depends on US1 completion (authentication required) - Can start once US1 is complete
- **Phase 5 (US3)**: Depends on US1 and US2 completion (needs authentication and ideas to exist) - Can start once US2 is complete
- **Phase 6 (US4)**: Depends on US1, US2, US3 completion (needs authentication, ideas, and viewing capabilities) - Can start once US3 is complete
- **Phase 7 (Polish)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: CRITICAL - Must complete first. All other stories require authentication.
- **User Story 2 (P2)**: Requires US1 (authentication). Once complete, enables idea creation.
- **User Story 3 (P3)**: Requires US1 (authentication) and US2 (ideas must exist to list/view).
- **User Story 4 (P4)**: Requires US1 (authentication), US2 (ideas must exist), US3 (viewing capability for evaluation context).

### Within Each User Story

1. **Tests first** (TDD approach per constitution):
   - Write unit tests (ensure they fail)
   - Write integration tests (ensure they fail)
   - Write e2e tests (ensure they fail)

2. **Implementation sequence**:
   - Models → migrations (database schema)
   - Repositories (data access)
   - Schemas (validation and serialization)
   - Services (business logic)
   - API endpoints (controllers)
   - Frontend components (UI)
   - Verify tests pass

3. **Story checkpoint**: Test independently before moving to next priority

### Parallel Opportunities

**Within Setup (Phase 1)**:
- T003, T004 can run in parallel (backend and frontend initialization)
- T008, T009 can run in parallel (test framework configuration)

**Within Foundational (Phase 2)**:
- T013, T014 can run in parallel (password hasher and JWT handler)
- T022, T023, T024 can run in parallel (frontend infrastructure)

**Within Each User Story**:
- All unit tests marked [P] can run in parallel (different test files)
- Models marked [P] can run in parallel (different entities)
- Schemas marked [P] can run in parallel (different schema files)
- Frontend components marked [P] can run in parallel (different component files)

**Across User Stories** (if team capacity allows):
- Once US1 is complete, US2 can begin
- If sufficient team members, after US2 completes: US3 and US4 could theoretically start in parallel (though US4 benefits from US3's viewing capabilities)

**Polish Phase**:
- T137, T138, T139, T140 can run in parallel (documentation, logging, rate limiting)
- T144, T145 can run in parallel (accessibility and responsive design)

---

## Parallel Example: User Story 1

```bash
# Launch all unit tests for User Story 1 together after writing them:
Task T025: "Unit test for User model validation"
Task T026: "Unit test for password_hasher utility"
Task T027: "Unit test for JWT handler utility"
Task T028: "Unit test for UserRepository CRUD"
Task T029: "Unit test for AuthService registration"
Task T030: "Unit test for AuthService login"
Task T031: "Unit test for auth middleware"

# Launch schema creation tasks together:
Task T041: "Create user request schemas"
Task T042: "Create user response schemas"

# Launch frontend component creation together:
Task T050: "Create registration form component"
Task T051: "Create login form component"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ Complete **Phase 1: Setup** (T001-T009)
2. ✅ Complete **Phase 2: Foundational** (T010-T024) - CRITICAL BLOCKER
3. ✅ Complete **Phase 3: User Story 1** (T025-T059)
4. **STOP and VALIDATE**: 
   - Run all US1 tests (unit, integration, e2e)
   - Manually test registration and login flows
   - Verify authentication works end-to-end
5. **Demo authentication system** or proceed to US2

### Incremental Delivery (Recommended)

1. **Foundation** (Setup + Foundational) → Infrastructure ready
2. **US1** (Authentication) → Test independently → Users can register and login ✅ **MVP**
3. **US2** (Idea Submission) → Test independently → Users can submit ideas ✅ **Core Value**
4. **US3** (Idea Listing) → Test independently → Transparency into submissions ✅
5. **US4** (Admin Evaluation) → Test independently → Complete evaluation loop ✅ **Full MVP**
6. **Polish** → Production-ready system ✅

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With **2 developers**:
1. Both complete Setup + Foundational together (T001-T024)
2. **Dev A**: User Story 1 (T025-T059)
3. Once US1 complete:
   - **Dev A**: User Story 2 (T060-T090)
   - **Dev B**: Can start preparing User Story 3 scaffolding (read-only tests and models)
4. Continue sequentially or overlap where possible

With **3+ developers**:
1. All complete Setup + Foundational together
2. **Dev A**: User Story 1 (blocking - must complete first)
3. Once US1 complete:
   - **Dev A**: User Story 2
   - **Dev B**: Can prepare User Story 3 (models, tests)
4. Once US2 complete:
   - **Dev B**: Complete User Story 3
   - **Dev C**: User Story 4
5. Stories integrate and test after each completion

---

## Test Coverage Targets (Per Constitution)

- **Overall**: 70% unit tests, 20% integration tests, 10% e2e tests
- **Critical Modules** (auth, ideas): Minimum **80% coverage**
- **TDD Approach**: Write tests first, implement to make them pass
- **Test Naming**: `test_action_condition_expectedResult` (e.g., `test_register_duplicateEmail_returns409`)

**Test Counts by User Story:**

- **US1 (Authentication)**: 13 unit tests, 5 integration tests, 1 e2e test = 19 tests
- **US2 (Idea Submission)**: 6 unit tests, 2 integration tests, 1 e2e test = 9 tests
- **US3 (Idea Listing)**: 3 unit tests, 3 integration tests, 1 e2e test = 7 tests
- **US4 (Admin Evaluation)**: 3 unit tests, 2 integration tests, 1 e2e test = 6 tests

**Total: 41 tests** (25 unit / 12 integration / 4 e2e = ~61% unit, ~29% integration, ~10% e2e - within acceptable ranges)

---

## Summary

- **Total Tasks**: 150 tasks
- **Tasks by Phase**:
  - Phase 1 (Setup): 9 tasks
  - Phase 2 (Foundational): 15 tasks
  - Phase 3 (US1 - Authentication): 35 tasks (19 tests + 16 implementation)
  - Phase 4 (US2 - Idea Submission): 31 tasks (9 tests + 22 implementation)
  - Phase 5 (US3 - Idea Listing): 24 tasks (7 tests + 17 implementation)
  - Phase 6 (US4 - Admin Evaluation): 22 tasks (6 tests + 16 implementation)
  - Phase 7 (Polish): 14 tasks

- **Parallelization**: 40+ tasks marked [P] for parallel execution
- **MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1 only) = 59 tasks for minimal viable authentication system
- **Full MVP**: All phases 1-6 = 136 tasks for complete feature set
- **Independent Testing**: Each user story can be tested independently at its checkpoint
- **TDD Compliance**: All test tasks precede implementation tasks per constitution

---

## Notes

- ✅ All tasks follow checklist format with ID, optional [P] marker, story label, and file paths
- ✅ Tasks organized by user story for independent implementation
- ✅ TDD approach enforced: tests written before implementation
- ✅ Each user story has independent test criteria
- ✅ Dependencies clearly documented
- ✅ Parallel opportunities identified
- ✅ Constitution compliance: 70/20/10 test pyramid, <30 lines per function, TDD mandatory
- ✅ Project structure matches plan.md (backend/ and frontend/ directories)
- ✅ All 29 functional requirements from spec.md mapped to tasks
- ✅ All 4 entities from data-model.md included
- ✅ All 12 API endpoints from contracts/ included
- ✅ Naming conventions follow constitution: `test_action_condition_expectedResult`

**Next Steps**: Execute tasks in order, starting with Phase 1 (Setup). Mark tasks complete as you progress. Stop at any checkpoint to validate story independence.
