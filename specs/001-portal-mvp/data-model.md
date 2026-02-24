# Data Model: InnovatEPAM Portal Phase 1 MVP

**Purpose**: Define entities, attributes, relationships, and validation rules  
**Date**: 2026-02-24  
**Input**: Requirements from spec.md and research.md technology decisions

---

## Entity Relationship Overview

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│    User     │         │     Idea     │         │  Evaluation  │
│             │1      * │              │1      * │              │
│ - id        │◄────────┤ - id         │◄────────┤ - id         │
│ - email     │ submits │ - title      │ has     │ - decision   │
│ - password  │         │ - description│         │ - comment    │
│ - name      │         │ - status     │         │ - created_at │
│ - role      │         │ - category   │         └──────────────┘
│ - created_at│         │ - attachment │              ▲
└─────────────┘         │ - created_at │              │
       │                │ - updated_at │              │ evaluates
       │                └──────────────┘              │
       │                       │                      │
       │                       │ categorized_by       │
       │                       ▼                      │
       │                ┌──────────────┐              │
       │                │   Category   │              │
       │                │              │              │
       │                │ - id         │              │
       │                │ - name       │              │
       │                │ - description│              │
       │                └──────────────┘              │
       │                                              │
       └──────────────────────────────────────────────┘
                    admin evaluates (role = admin)
```

**Relationships**:
- User (1) → (M) Idea: A user can submit many ideas
- Idea (1) → (M) Evaluation: An idea can have multiple evaluations (status changes)
- User (1) → (M) Evaluation: An admin can create many evaluations
- Category (1) → (M) Idea: Each idea belongs to one category

---

## Entity Definitions

### 1. User Entity

**Purpose**: Represents system users with authentication credentials and role-based access

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique user identifier |
| `email` | String(255) | Unique, Not Null, Valid email format | User's email address (login credential) |
| `hashed_password` | String(255) | Not Null | bcrypt hashed password (NEVER store plain text) |
| `full_name` | String(100) | Not Null | User's full name for display |
| `role` | Enum('submitter', 'admin') | Not Null, Default='submitter' | User's access level |
| `is_active` | Boolean | Not Null, Default=True | Account status (for future deactivation) |
| `created_at` | DateTime | Not Null, Auto-generated | Account creation timestamp |
| `updated_at` | DateTime | Not Null, Auto-updated | Last profile update timestamp |

**Validation Rules**:
- Email must be valid format (regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`)
- Email must be unique across all users (case-insensitive)
- Password must meet complexity requirements (defined in service layer):
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
  - At least 1 special character
- Full name: 2-100 characters, no special characters except spaces, hyphens, apostrophes
- Role restricted to enum values only

**Indexes**:
- Primary: `id` (clustered)
- Unique: `email` (lowercase)
- Index: `role` (for admin queries)

**Security Considerations**:
- Password field NEVER returned in API responses
- hashed_password uses bcrypt with 12 rounds
- Email stored in lowercase for case-insensitive lookups

---

### 2. Category Entity

**Purpose**: Predefined classification system for ideas

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique category identifier |
| `name` | String(50) | Unique, Not Null | Category display name |
| `description` | String(255) | Nullable | Brief category explanation |
| `display_order` | Integer | Not Null, Default=0 | Sort order for UI display |
| `is_active` | Boolean | Not Null, Default=True | Visibility in idea submission |
| `created_at` | DateTime | Not Null, Auto-generated | Category creation timestamp |

**Initial Seed Data** (Phase 1):
```python
categories = [
    {"name": "Process Improvement", "description": "Ideas to streamline workflows and procedures", "display_order": 1},
    {"name": "Technology Innovation", "description": "New tools, platforms, or technical solutions", "display_order": 2},
    {"name": "Cost Reduction", "description": "Ideas to reduce expenses or improve efficiency", "display_order": 3},
    {"name": "Customer Experience", "description": "Improvements to client interactions and satisfaction", "display_order": 4},
    {"name": "Employee Experience", "description": "Workplace improvements and team culture", "display_order": 5},
    {"name": "Other", "description": "Ideas that don't fit other categories", "display_order": 99},
]
```

**Validation Rules**:
- Name: 3-50 characters, alphanumeric with spaces
- Name must be unique (case-insensitive)
- Description: 0-255 characters

**Indexes**:
- Primary: `id`
- Unique: `name` (lowercase)
- Index: `display_order, is_active` (for sorted active category lists)

**Notes**:
- Categories are system-managed in Phase 1 (no user creation)
- Inactive categories don't appear in submission form but remain for historical ideas
- Future phases may add user-suggested categories pending admin approval

---

### 3. Idea Entity

**Purpose**: Innovation proposals submitted by users

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique idea identifier |
| `title` | String(200) | Not Null | Brief idea title/headline |
| `description` | Text | Not Null | Detailed idea description |
| `category_id` | UUID | Foreign Key → Category.id, Not Null | Associated category |
| `submitter_id` | UUID | Foreign Key → User.id, Not Null | User who submitted idea |
| `status` | Enum('submitted', 'under_review', 'accepted', 'rejected') | Not Null, Default='submitted' | Current evaluation state |
| `attachment_filename` | String(255) | Nullable | Original uploaded filename |
| `attachment_path` | String(500) | Nullable | Storage path/URL for file |
| `attachment_size` | Integer | Nullable | File size in bytes |
| `attachment_mimetype` | String(100) | Nullable | File MIME type |
| `created_at` | DateTime | Not Null, Auto-generated | Idea submission timestamp |
| `updated_at` | DateTime | Not Null, Auto-updated | Last modification timestamp |

**Validation Rules**:
- Title: 10-200 characters, required
- Description: 50-5000 characters, required
- Attachment (if provided):
  - Size: Maximum 10MB (10,485,760 bytes)
  - Allowed MIME types: 
    - Documents: `application/pdf`, `application/msword`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
    - Spreadsheets: `application/vnd.ms-excel`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
    - Images: `image/jpeg`, `image/png`, `image/gif`
  - Blocked: Executables, scripts, archives
- Status transitions (enforced in service layer):
  - `submitted` → `under_review` (admin only)
  - `submitted` → `accepted` (admin only, requires comment)
  - `submitted` → `rejected` (admin only, requires comment)
  - `under_review` → `accepted` (admin only, requires comment)
  - `under_review` → `rejected` (admin only, requires comment)
  - `accepted/rejected` → any status (admin only, allows re-evaluation)

**Indexes**:
- Primary: `id`
- Foreign Key: `category_id`
- Foreign Key: `submitter_id`
- Index: `status` (for filtering by evaluation state)
- Index: `submitter_id, created_at DESC` (for user's idea list)
- Index: `created_at DESC` (for admin all-ideas list)

**Constraints**:
- If attachment fields present, all must be populated together (filename, path, size, mimetype)
- On submitter User deletion: SET NULL or CASCADE DELETE (decision needed)
- On Category deletion: RESTRICT (cannot delete category with ideas)

**Security Considerations**:
- Attachment path should not expose internal filesystem structure in API responses
- File downloads require authentication and authorization check (user owns idea OR user is admin)
- Filename sanitization prevents path traversal attacks

---

### 4. Evaluation Entity

**Purpose**: Admin assessments and status changes for ideas

**Attributes**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | Primary Key, Auto-generated | Unique evaluation identifier |
| `idea_id` | UUID | Foreign Key → Idea.id, Not Null | Evaluated idea |
| `evaluator_id` | UUID | Foreign Key → User.id, Not Null | Admin who performed evaluation |
| `previous_status` | Enum('submitted', 'under_review', 'accepted', 'rejected') | Not Null | Status before evaluation |
| `new_status` | Enum('submitted', 'under_review', 'accepted', 'rejected') | Not Null | Status after evaluation |
| `comment` | Text | Not Null | Admin's feedback/reasoning |
| `created_at` | DateTime | Not Null, Auto-generated | Evaluation timestamp |

**Validation Rules**:
- Comment: 10-2000 characters, required
- previous_status must match idea's current status at evaluation time (enforced by service layer)
- new_status must be different from previous_status
- evaluator must have role='admin' (enforced by service layer)

**Indexes**:
- Primary: `id`
- Foreign Key: `idea_id`
- Foreign Key: `evaluator_id`
- Index: `idea_id, created_at DESC` (for idea evaluation history)

**Constraints**:
- On Idea deletion: CASCADE DELETE (remove evaluation history with idea)
- On User deletion: SET NULL or CASCADE DELETE for evaluator (decision needed)

**Business Rules**:
- Each status change creates a new Evaluation record (audit trail)
- Evaluations are immutable once created (no updates/deletes)
- Only most recent evaluation's new_status reflects idea's current status
- Evaluation history visible to:
  - Idea submitter (their own ideas)
  - All admins (all ideas)

---

## Derived/Computed Values

These are NOT stored in database but calculated on-demand:

| Value | Calculation | Purpose |
|-------|-------------|---------|
| `idea.evaluation_count` | `COUNT(evaluations WHERE idea_id = idea.id)` | Show evaluation activity |
| `idea.current_evaluator` | `evaluator_id FROM latest evaluation` | Shows who last evaluated |
| `idea.current_evaluation_comment` | `comment FROM latest evaluation` | Current feedback |
| `user.submitted_ideas_count` | `COUNT(ideas WHERE submitter_id = user.id)` | User activity metric |
| `user.ideas_by_status` | Group ideas by status for user | Dashboard summary |

---

## State Transitions

### Idea Status Lifecycle

```
                    ┌──────────────┐
                    │  submitted   │ (Initial state)
                    └──────┬───────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
       ┌────────────────┐    ┌────────────┐
       │  under_review  │    │  accepted  │
       └────────┬───────┘    └────────────┘
                │
                ▼
       ┌────────────────┐
       │    rejected    │
       └────────────────┘

Note: Admin can transition between any statuses (allows re-evaluation)
```

**State Change Authorization**:
- Submitters: READ-ONLY (cannot change status)
- Admins: FULL CONTROL (any status → any status)

---

## Sample Database Queries

**Common Access Patterns**:

1. **User Registration**:
```sql
INSERT INTO users (id, email, hashed_password, full_name, role, created_at, updated_at)
VALUES (gen_random_uuid(), $1, $2, $3, 'submitter', NOW(), NOW());
```

2. **User Login**:
```sql
SELECT id, email, hashed_password, full_name, role, is_active
FROM users
WHERE LOWER(email) = LOWER($1) AND is_active = TRUE;
```

3. **List Ideas (Submitter)**:
```sql
SELECT i.id, i.title, i.status, i.created_at, c.name as category_name
FROM ideas i
JOIN categories c ON i.category_id = c.id
WHERE i.submitter_id = $1
ORDER BY i.created_at DESC
LIMIT 50 OFFSET $2;
```

4. **List Ideas (Admin)**:
```sql
SELECT i.id, i.title, i.status, i.created_at, c.name as category_name,
       u.full_name as submitter_name, u.email as submitter_email
FROM ideas i
JOIN categories c ON i.category_id = c.id
JOIN users u ON i.submitter_id = u.id
ORDER BY i.created_at DESC
LIMIT 50 OFFSET $1;
```

5. **Get Idea Detail with Latest Evaluation**:
```sql
SELECT i.*, c.name as category_name, u.full_name as submitter_name,
       e.comment as latest_comment, e.created_at as evaluated_at,
       evaluator.full_name as evaluator_name
FROM ideas i
JOIN categories c ON i.category_id = c.id
JOIN users u ON i.submitter_id = u.id
LEFT JOIN LATERAL (
    SELECT * FROM evaluations
    WHERE idea_id = i.id
    ORDER BY created_at DESC
    LIMIT 1
) e ON TRUE
LEFT JOIN users evaluator ON e.evaluator_id = evaluator.id
WHERE i.id = $1;
```

6. **Create Evaluation**:
```sql
-- Transaction required:
BEGIN;
  INSERT INTO evaluations (id, idea_id, evaluator_id, previous_status, new_status, comment, created_at)
  VALUES (gen_random_uuid(), $1, $2, $3, $4, $5, NOW());
  
  UPDATE ideas SET status = $4, updated_at = NOW()
  WHERE id = $1 AND status = $3;  -- Prevent race conditions
COMMIT;
```

---

## Data Migration Strategy

**Phase 1 Migrations** (using Alembic):

1. **Migration 001**: Create users table
2. **Migration 002**: Create categories table + seed initial categories
3. **Migration 003**: Create ideas table with foreign keys
4. **Migration 004**: Create evaluations table with foreign keys
5. **Migration 005**: Create indexes for performance

**Rollback Strategy**: Each migration has down() function to reverse changes

---

## Data Retention & Archival

**Phase 1 (MVP)**:
- No automatic deletion or archival
- All data retained indefinitely
- Manual cleanup via admin tooling if needed

**Future Considerations**:
- Soft delete for users (is_active = false)
- Archive old ideas after N years
- GDPR compliance for data export/deletion requests

---

**Status**: Data model complete with validation rules and relationships. Ready for contract definition.
