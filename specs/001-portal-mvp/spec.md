# Feature Specification: InnovatEPAM Portal Phase 1 MVP

**Feature Branch**: `001-portal-mvp`  
**Created**: 2026-02-24  
**Status**: Draft  
**Input**: User description: "InnovatEPAM Portal Phase 1 MVP - User Management (Register, Login, Logout, Role distinction submitter/admin), Idea Submission (Create with title/description/category, Single file attachment, List ideas), Evaluation Workflow (Status: submitted/under_review/accepted/rejected, Admin accept/reject with comment)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1)

Users need to create accounts and securely log in to access the portal. This foundational capability enables all other features by establishing user identity and role-based access control.

**Why this priority**: Without authentication, no other features can function. This is the foundational layer that enables secure access to the system and establishes user roles (submitter vs admin) that drive all subsequent workflows.

**Independent Test**: Can be fully tested by registering a new user account, logging in with credentials, verifying role assignment, and logging out. Delivers value by allowing users to establish secure portal access.

**Acceptance Scenarios**:

1. **Given** no existing account, **When** user provides valid email, password, and name, **Then** account is created with "submitter" role and user can log in
2. **Given** valid credentials, **When** user attempts to log in, **Then** user is authenticated and sees their role-appropriate dashboard
3. **Given** authenticated user, **When** user clicks logout, **Then** session is terminated and user is returned to login screen
4. **Given** existing email, **When** new user tries to register with same email, **Then** registration is rejected with clear error message
5. **Given** invalid password format, **When** user tries to register, **Then** system provides password requirements feedback
6. **Given** incorrect password, **When** user tries to log in, **Then** authentication fails with generic error (no email confirmation for security)

---

### User Story 2 - Idea Submission by Users (Priority: P2)

Submitters need to create and submit innovation ideas with relevant details. This is the core value proposition of the portal - capturing employee ideas for evaluation.

**Why this priority**: This is the primary business function. Once users can authenticate, submitting ideas is the most critical user action. Without this, the portal has no purpose.

**Independent Test**: Can be fully tested by logging in as a submitter, creating an idea with title/description/category/attachment, and verifying it appears in the idea list. Delivers value by enabling innovation capture.

**Acceptance Scenarios**:

1. **Given** authenticated submitter, **When** user fills in idea title, description, category, and optional file attachment, **Then** idea is created with "submitted" status
2. **Given** idea creation form, **When** user provides title and description but no category, **Then** system prompts for category selection
3. **Given** file attachment field, **When** user attaches a single file under size limit, **Then** file is uploaded and linked to idea
4. **Given** file attachment field, **When** user tries to attach file exceeding size limit, **Then** system rejects with clear size limit message
5. **Given** authenticated submitter, **When** user views ideas list, **Then** all their submitted ideas are visible with status indicators

---

### User Story 3 - Idea List and Viewing (Priority: P3)

Users need to view and browse submitted ideas. Submitters see their own ideas; admins see all ideas for evaluation.

**Why this priority**: Visibility into submitted ideas is essential but secondary to actually submitting ideas. Users can submit ideas without immediately viewing the full list, but need this for tracking progress.

**Independent Test**: Can be fully tested by submitting multiple ideas and verifying they appear in the list with correct details (title, status, submission date). Delivers value by providing transparency into submitted ideas.

**Acceptance Scenarios**:

1. **Given** authenticated submitter, **When** user navigates to ideas list, **Then** only their submitted ideas are displayed
2. **Given** authenticated admin, **When** user navigates to ideas list, **Then** all submitted ideas from all users are displayed
3. **Given** ideas list, **When** user clicks on an idea, **Then** full idea details (title, description, category, attachment, status) are displayed
4. **Given** multiple ideas, **When** list is displayed, **Then** ideas show submission date, status, and basic metadata
5. **Given** no submitted ideas, **When** user views list, **Then** system displays helpful message prompting idea submission

---

### User Story 4 - Admin Evaluation Workflow (Priority: P4)

Admins need to review submitted ideas and make accept/reject decisions with feedback comments. This closes the evaluation loop and provides feedback to submitters.

**Why this priority**: While critical for the complete workflow, evaluation can happen asynchronously after ideas are submitted. Initial MVP value is delivered when users can submit ideas, even if evaluation is manual/offline initially.

**Independent Test**: Can be fully tested by logging in as admin, viewing submitted ideas, and accepting or rejecting an idea with a comment. Delivers value by enabling formal evaluation and feedback.

**Acceptance Scenarios**:

1. **Given** authenticated admin viewing an idea with "submitted" status, **When** admin clicks "Accept" and provides comment, **Then** idea status changes to "accepted" and comment is saved
2. **Given** authenticated admin viewing an idea with "submitted" status, **When** admin clicks "Reject" and provides comment, **Then** idea status changes to "rejected" and comment is saved
3. **Given** idea in "submitted" status, **When** admin begins review, **Then** status can optionally change to "under_review" to signal active evaluation
4. **Given** evaluated idea, **When** submitter views their idea, **Then** current status and admin comment are visible
5. **Given** idea in "accepted" or "rejected" status, **When** admin tries to change evaluation, **Then** system allows status change (evaluation is not immutable)
6. **Given** admin evaluation action, **When** admin attempts to save without comment, **Then** system requires comment for accept/reject decisions

---

### Edge Cases

- What happens when a user tries to register with an already-used email address?
- How does the system handle file uploads that exceed the maximum allowed size?
- What occurs if a user's session expires while filling out an idea submission form?
- How are ideas displayed when no ideas have been submitted yet?
- What happens if an admin attempts to evaluate an idea that has already been evaluated?
- How does the system handle special characters or very long text in idea titles and descriptions?
- What occurs when a file attachment is corrupted or has an unsupported file type?
- How are role assignments verified when users attempt to access admin-only functions?

## Requirements *(mandatory)*

### Functional Requirements

**User Management**

- **FR-001**: System MUST allow new users to register with email, password, and full name
- **FR-002**: System MUST validate email format and ensure email uniqueness across all users
- **FR-003**: System MUST hash and securely store passwords (never in plain text)
- **FR-004**: System MUST authenticate users via email and password credentials
- **FR-005**: System MUST assign one of two roles to each user: "submitter" or "admin"
- **FR-006**: System MUST provide logout functionality that terminates user sessions
- **FR-007**: System MUST enforce password complexity requirements (minimum length, character variety)
- **FR-008**: System MUST prevent unauthorized access to role-specific features

**Idea Submission**

- **FR-009**: System MUST allow authenticated submitters to create new ideas
- **FR-010**: System MUST require title, description, and category for each idea submission
- **FR-011**: System MUST support a predefined list of categories for idea classification
- **FR-012**: System MUST allow optional file attachment (single file) for each idea
- **FR-013**: System MUST enforce file size limits for attachments
- **FR-014**: System MUST automatically set idea status to "submitted" upon creation
- **FR-015**: System MUST timestamp each idea with submission date
- **FR-016**: System MUST associate each idea with the submitter's user account

**Idea Listing and Viewing**

- **FR-017**: System MUST display a list of ideas to authenticated users
- **FR-018**: System MUST show submitters only their own ideas in the list
- **FR-019**: System MUST show admins all ideas from all users in the list
- **FR-020**: System MUST display idea metadata (title, status, submission date) in list view
- **FR-021**: System MUST provide detail view showing full idea information (title, description, category, attachment, status, comments)

**Evaluation Workflow**

- **FR-022**: System MUST support four idea statuses: "submitted", "under_review", "accepted", "rejected"
- **FR-023**: System MUST allow admins to change idea status from "submitted" to "under_review"
- **FR-024**: System MUST allow admins to accept ideas (change status to "accepted") with mandatory comment
- **FR-025**: System MUST allow admins to reject ideas (change status to "rejected") with mandatory comment
- **FR-026**: System MUST store admin comments associated with evaluation decisions
- **FR-027**: System MUST display evaluation status and admin comments to idea submitters
- **FR-028**: System MUST allow status changes on previously evaluated ideas (evaluations are not immutable)
- **FR-029**: System MUST restrict evaluation actions (accept/reject/review) to admin role only

### Key Entities

- **User**: Represents a system user with authentication credentials (email, hashed password), profile information (full name), and role assignment (submitter or admin). Users can own multiple ideas if they are submitters.

- **Idea**: Represents an innovation proposal submitted by a user. Contains descriptive content (title, description, category), optional file attachment, metadata (submission timestamp, current status), and relationship to submitting user. Tracks evaluation history through status and admin comments.

- **Category**: Represents a classification for ideas. Predefined list of innovation categories (e.g., "Process Improvement", "Technology Innovation", "Cost Reduction", "Customer Experience") used for organizing and filtering ideas.

- **Evaluation**: Represents an admin's assessment of an idea. Contains decision (accept/reject), optional status change (under_review), mandatory comment providing feedback, and relationship to evaluating admin and evaluated idea.

### Assumptions

- **Auth Method**: Email/password authentication is sufficient for Phase 1 MVP. SSO and OAuth integration are deferred to future phases.
- **File Types**: File attachment accepts common document formats (PDF, DOCX, XLSX, images). Executable files are blocked for security.
- **File Size Limit**: Maximum file attachment size is 10MB (reasonable for documents/images while preventing storage abuse).
- **Category Management**: Categories are system-defined and managed by configuration. User-created categories are not supported in Phase 1.
- **Role Assignment**: Initial admin accounts are created manually or through configuration. Self-service admin role requests are not supported in Phase 1.
- **Session Management**: Standard session timeout of 30 minutes of inactivity. Remember-me functionality is not included in Phase 1.
- **Notifications**: Email or in-app notifications for idea status changes are deferred to future phases. Users check status manually.
- **Idea Editing**: Once submitted, ideas cannot be edited by submitters. This prevents evaluation confusion. Editing may be added in future phases.
- **Multi-file Attachments**: Single file attachment per idea in Phase 1. Multiple attachments deferred to future phases.
- **Search and Filtering**: Advanced search and filtering of ideas list is not included in Phase 1. Basic list display only.

## Success Criteria *(mandatory)*

### Measurable Outcomes

**User Experience**

- **SC-001**: Users can complete account registration in under 3 minutes from landing page to successful login
- **SC-002**: Users can submit a complete idea (with all required fields and attachment) in under 5 minutes
- **SC-003**: 90% of users successfully complete account registration on their first attempt without support
- **SC-004**: Idea submission success rate exceeds 95% (excluding intentional validation failures)

**System Performance**

- **SC-005**: System handles at least 100 concurrent users without response time degradation
- **SC-006**: Idea list loads within 2 seconds for users with up to 100 ideas
- **SC-007**: File upload completes within 10 seconds for files up to 10MB
- **SC-008**: Authentication response time is under 1 second for valid credentials

**Business Value**

- **SC-009**: Portal enables collection of at least 50 ideas within first month of deployment
- **SC-010**: Admin evaluation workflow reduces idea processing time by 40% compared to manual/email-based process
- **SC-011**: 80% of submitters can find and view their idea status without requiring support assistance
- **SC-012**: Zero security incidents related to authentication or authorization in first 3 months

**Quality and Reliability**

- **SC-013**: System maintains 99% uptime during business hours (weekdays 8 AM - 6 PM)
- **SC-014**: Password security meets industry standards (hashing with bcrypt or Argon2, no plain text storage)
- **SC-015**: Role-based access control prevents 100% of unauthorized access attempts (users cannot access admin functions)
- **SC-016**: File upload validation prevents 100% of oversized or malicious file uploads

**User Satisfaction**

- **SC-017**: System receives average user satisfaction score of 4 out of 5 or higher in post-launch survey
- **SC-018**: Submitters report clear understanding of their idea status without confusion
- **SC-019**: Admins report that evaluation workflow is more efficient than previous process
- **SC-020**: Less than 5% of users report difficulty logging in or accessing features they need
