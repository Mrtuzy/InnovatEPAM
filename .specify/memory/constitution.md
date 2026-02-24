<!--
SYNC IMPACT REPORT
==================
Version Change: INITIAL → 1.0.0
Constitution Type: Initial ratification for InnovatEPAM Portal

Modified Principles:
- NEW: I. Clean Architecture & Separation of Concerns
- NEW: II. RESTful API Design
- NEW: III. Test-First Development (NON-NEGOTIABLE)
- NEW: IV. Code Quality Standards
- NEW: V. Security-First Approach

Added Sections:
- Testing Strategy (detailed pyramid structure)
- Naming Conventions
- Development Workflow

Templates Status:
- ✅ plan-template.md: Constitution Check gates compatible
- ✅ spec-template.md: User story priorities align with testing requirements
- ✅ tasks-template.md: Task categorization supports principle-driven development

Follow-up Actions: NONE - All placeholders resolved
-->

# InnovatEPAM Portal Constitution

## Core Principles

### I. Clean Architecture & Separation of Concerns

**MUST enforce clear architectural boundaries throughout the system:**

- Business logic MUST be isolated from framework-specific code
- Controllers MUST NOT contain business logic - they orchestrate only
- Each layer MUST depend only on abstractions, not concrete implementations
- Domain models MUST be independent of infrastructure concerns
- Services layer handles business rules; repositories handle data access

**Rationale**: Clean architecture ensures maintainability, testability, and flexibility to evolve the system without cascading changes. Separating concerns prevents tight coupling and enables independent testing of business logic.

### II. RESTful API Design

**MUST follow RESTful principles for all API endpoints:**

- Resources identified by nouns (e.g., `/ideas`, `/users`, not `/getIdea`)
- Standard HTTP methods: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
- Proper HTTP status codes: 200 (OK), 201 (Created), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 500 (Server Error)
- Stateless communication - each request contains all necessary information
- Consistent resource naming and URL structure
- API versioning strategy (e.g., `/api/v1/ideas`)

**Rationale**: RESTful design provides predictable, standardized interfaces that are easier to consume, document, and maintain. It aligns with web standards and facilitates integration with various clients.

### III. Test-First Development (NON-NEGOTIABLE)

**TDD approach is MANDATORY for all new features:**

- RED → GREEN → REFACTOR cycle strictly enforced
- Tests MUST be written before implementation code
- Tests MUST be meaningful and able to fail - no tautological assertions
- Minimum 80% code coverage required for authentication and idea modules
- All tests MUST follow the naming convention: `test_action_condition_expectedResult`

**Testing Pyramid Distribution:**
- 70% Unit tests (fast, isolated, test individual components)
- 20% Integration tests (test component interactions)
- 10% End-to-end tests (test complete user journeys)

**Rationale**: TDD ensures code is designed for testability from the start, catches defects early, serves as living documentation, and reduces regressions. The pyramid structure optimizes test execution speed and maintenance cost while providing comprehensive coverage.

### IV. Code Quality Standards

**MUST maintain high code quality through enforceable standards:**

- Linting MUST pass before commits (no warnings or errors allowed)
- Functions MUST be small and focused (maximum 30 lines)
- Single Responsibility Principle - each function/class has one reason to change
- Meaningful variable and function names (self-documenting code)
- Code reviews required for all changes
- No commented-out code in production branches
- DRY principle - avoid duplication, extract reusable components

**Rationale**: Small, focused functions are easier to understand, test, and maintain. Linting catches common issues early. Code quality standards reduce technical debt and onboarding time for new developers.

### V. Security-First Approach

**Security MUST be built into every layer of the application:**

- Password hashing MUST use industry-standard algorithms (bcrypt, Argon2, or PBKDF2)
- NEVER store passwords in plain text or use weak hashing (MD5, SHA1)
- Role-Based Access Control (RBAC) MUST be implemented and enforced
- Authorization checks required before any protected resource access
- Input validation and sanitization MUST be performed on all user inputs
- SQL injection prevention through parameterized queries or ORM
- XSS prevention through output encoding
- HTTPS required for all production endpoints
- Sensitive data (tokens, secrets) MUST NOT be logged or exposed

**Rationale**: Security breaches have severe consequences including data loss, legal liability, and reputation damage. Security must be considered from the design phase, not added as an afterthought. RBAC ensures proper access control and audit trails.

## Testing Strategy

**Pyramid Structure Breakdown:**

**Unit Tests (70%)**
- Test individual functions, methods, classes in isolation
- Mock external dependencies
- Fast execution (milliseconds per test)
- Focus areas: business logic, utility functions, validators, formatters

**Integration Tests (20%)**
- Test interactions between components
- Use test databases or containers
- Verify API contracts between layers
- Focus areas: repository layer, service layer interactions, API endpoints

**End-to-End Tests (10%)**
- Test complete user workflows
- Use production-like environment
- Validate critical user journeys
- Focus areas: authentication flow, idea submission flow, approval workflows

**Coverage Requirements:**
- Authentication module: minimum 80% coverage
- Idea management module: minimum 80% coverage
- Other modules: recommended 70% coverage

**Test Quality Standards:**
- Every assertion MUST be able to fail given wrong implementation
- Tests MUST be independent (no test depends on another test's state)
- Tests MUST be deterministic (same input → same result)
- Test data MUST be self-contained (no shared state between tests)

## Naming Conventions

**Test Naming Convention:**

Format: `test_action_condition_expectedResult`

Examples:
- `test_createIdea_validData_returnsCreatedIdea`
- `test_login_invalidPassword_returnsUnauthorized`
- `test_getUserById_nonExistentId_throwsNotFoundException`
- `test_submitIdea_unauthenticatedUser_returnsForbidden`
- `test_calculateScore_negativeInput_throwsValidationError`

**Additional Naming Standards:**
- Classes: PascalCase (e.g., `IdeaService`, `UserRepository`)
- Functions/Methods: camelCase (e.g., `createIdea`, `validateUser`)
- Constants: UPPER_SNAKE_CASE (e.g., `MAX_RETRY_COUNT`, `API_BASE_URL`)
- Private members: prefix with underscore (e.g., `_privateMethod`)
- Boolean variables: prefix with `is`, `has`, `should` (e.g., `isValid`, `hasPermission`)

## Development Workflow

**Code Review Gates:**
- All PRs require at least one approval
- Linting must pass (automated check)
- All tests must pass (automated check)
- Coverage thresholds must be met for auth and idea modules
- No direct commits to main/production branches

**Definition of Done:**
- Feature implementation complete
- Unit tests written and passing (TDD compliance)
- Integration tests added where applicable
- Code reviewed and approved
- Documentation updated (API docs, README)
- Manual testing completed for UI changes
- No known bugs or security issues

**Branch Strategy:**
- Feature branches: `###-feature-name`
- Hotfix branches: `hotfix-description`
- Main branch: protected, production-ready code only

## Governance

**Constitution Authority:**
- This constitution supersedes all other development practices and guidelines
- All code reviews MUST verify compliance with constitutional principles
- Any deviation from these principles MUST be explicitly justified and documented
- Complexity that violates principles requires architectural review and approval

**Amendment Process:**
- Constitutional changes require team consensus
- Amendments MUST include rationale and impact analysis
- Version must be incremented following semantic versioning:
  - MAJOR: Breaking changes to principles, removals, or backward-incompatible governance
  - MINOR: New principles added or substantial expansions
  - PATCH: Clarifications, wording improvements, non-semantic refinements
- After amendments, dependent templates and documentation MUST be synchronized
- All team members MUST be notified of constitutional changes

**Compliance Review:**
- Constitution compliance is checked during PR reviews
- Quarterly architecture reviews ensure adherence to principles
- Violations tracked and addressed in retrospectives
- New team members MUST review and acknowledge this constitution

**Version**: 1.0.0 | **Ratified**: 2026-02-24 | **Last Amended**: 2026-02-24
