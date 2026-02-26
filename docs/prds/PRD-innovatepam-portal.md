# Product Requirements Document (PRD)

**Project:** InnovatEPAM Portal
**Author:** GitHub Copilot
**Status:** Draft
**Version:** 1.0
**Last Updated:** 2026-02-24

---

## 1. Overview

### Purpose
This document defines the Phase 1 MVP requirements for the InnovatEPAM Portal, an AI-native platform that centralizes idea submission, evaluation, and status tracking for internal employee innovation workflows.

### Problem Statement
EPAM’s idea intake and evaluation process is currently fragmented across email threads and spreadsheets, creating poor visibility, slow evaluation cycles, and lost context for both submitters and evaluators. Based on typical enterprise intake workflows, teams can lose 3–5 hours per admin per week in manual triage and follow-up *(assumed — validate with data)*, while submitters lack transparent status updates, leading to lower engagement and repeated follow-up requests.

### Goals
- Reduce median idea evaluation cycle time (submission to decision) by 40% within 3 months of MVP launch.
- Increase employee idea program participation rate by 25% within 2 quarters by making submission and tracking transparent.
- Decrease admin time spent on manual status coordination and follow-up by 50% within 3 months.

---

## 2. User Personas

> Who are we building this for?

### Persona 1: Deniz, the Employee Submitter
- **Role:** Submitter (EPAM employee)
- **Description:** Individual contributor who proposes process, delivery, or product innovation ideas and needs visibility into evaluation progress.
- **Needs:** Quickly submit structured ideas with supporting evidence and track status without messaging managers directly.
- **Pain Points:** Unclear submission channels, no standardized format, and no reliable way to know whether an idea is being reviewed.

### Persona 2: Elif, the Innovation Program Manager
- **Role:** Admin / Evaluator
- **Description:** Manager responsible for triaging incoming ideas, coordinating review outcomes, and maintaining fair, auditable evaluation decisions.
- **Needs:** A centralized dashboard to review submissions, add comments, and move ideas through statuses consistently.
- **Pain Points:** Manual aggregation from multiple tools, duplicated review effort, and inconsistent communication back to submitters.

### Persona 3: Murat, the Engineering Lead Stakeholder
- **Role:** Stakeholder / Domain reviewer
- **Description:** Technical lead who reviews selected ideas for feasibility and implementation impact.
- **Needs:** Access to complete idea context and evaluator comments to provide timely technical feedback.
- **Pain Points:** Missing attachments or context spread across channels, causing delayed and lower-quality decisions.

---

## 3. Use Cases

> Key scenarios the system must support.

### UC-01: Submit New Idea
- **Actor:** Deniz (Submitter)
- **Precondition:** User is authenticated and has Submitter role.
- **Steps:**
  1. User opens the "Submit Idea" form.
  2. User enters title, description, and category.
  3. User uploads one supporting file attachment.
  4. User clicks "Submit" and confirms.
- **Postcondition / Expected Outcome:** Idea record is created with status `Submitted`, attachment is linked, and user sees confirmation.

### UC-02: Review and Decide on Idea
- **Actor:** Elif (Admin)
- **Precondition:** Admin is authenticated and at least one idea exists in `Submitted` or `Under Review` state.
- **Steps:**
  1. Admin opens the evaluation dashboard.
  2. Admin filters/selects an idea in `Submitted` status.
  3. Admin reads details and attachment, then adds evaluation comments.
  4. Admin updates status to `Under Review`, then to `Accepted` or `Rejected`.
- **Postcondition / Expected Outcome:** Decision and comments are saved in audit history and visible to the submitter.

### UC-03: Track Idea Status Transparently
- **Actor:** Deniz (Submitter)
- **Precondition:** Submitter has at least one submitted idea.
- **Steps:**
  1. User navigates to "My Ideas" list.
  2. User views each idea’s current status and last update timestamp.
  3. User opens a specific idea to read admin comments.
- **Postcondition / Expected Outcome:** User understands current decision stage and does not need manual follow-up.

### UC-04: Handle Invalid Attachment Upload (Edge Case)
- **Actor:** Deniz (Submitter)
- **Precondition:** User is authenticated and filling the idea form.
- **Steps:**
  1. User attempts to upload a file exceeding the 10MB size limit or using a non-supported format.
  2. System validates file client-side and server-side.
  3. System blocks submission and shows a specific validation error with allowed file rules (`pdf`, `png`, `jpg`, `jpeg`; max 10MB).
  4. User replaces the file with a valid one and resubmits.
- **Postcondition / Expected Outcome:** Invalid file is rejected safely; successful submission proceeds only with valid attachment.

---

## 4. Functional Requirements

> What the system must do.

| ID     | Requirement                          | Priority        | Notes                  |
|--------|--------------------------------------|-----------------|------------------------|
| FR-01  | The system shall support secure user registration and login for employees. | High | JWT-based authentication per technical context. |
| FR-02  | The system shall enforce role-based access control for `Submitter` and `Admin` roles across UI and APIs. | High | Prevent unauthorized admin actions. |
| FR-03  | The system shall provide an idea submission form with required fields: title, description, and category. | High | Required fields validated before submit. |
| FR-04  | The system shall allow exactly one file attachment per idea submission in Phase 1 MVP. | High | Allowed formats: `pdf`, `png`, `jpg`, `jpeg`; maximum size: 10MB. |
| FR-05  | The system shall display an idea listing view showing status and last updated timestamp to authorized users. | High | Submitter view includes own ideas; admin view includes all ideas. |
| FR-06  | The system shall support status transitions: `Submitted` → `Under Review` → (`Accepted` or `Rejected`). | High | Transition rules must be enforced by backend. |
| FR-07  | The system shall allow admins to add decision comments when accepting or rejecting an idea. | High | Comments required for `Rejected` *(assumed — validate policy)*. |
| FR-08  | The system shall allow admins to reopen ideas in `Accepted` or `Rejected` state by transitioning them back to `Under Review` with a mandatory reopen reason. | Med | Reopen action must be role-restricted and auditable. |
| FR-09  | The system must record a timestamped audit trail for status changes and evaluator comments. | Med | Supports transparency and governance. |
| FR-10  | The system shall expose API and UI behaviors that are testable with minimum 80% automated test coverage for MVP modules. | Med | Matches AI-native engineering standards. |

---

## 5. Non-Functional Requirements

> Quality attributes the system must satisfy.

### Performance
- API read operations must respond within 300ms at p95 under normal MVP load *(default — confirm with engineering)*.
- Idea submission requests (including single-file upload) must complete within 2.5 seconds at p95 for files up to 10MB *(default — confirm with engineering)*.

### Security
- All data in transit must be encrypted using TLS 1.2+.
- Authentication must use signed JWTs with expiration and server-side validation on every protected API request.
- Role checks must be enforced server-side for all status-change and moderation endpoints.

### Reliability & Availability
- System uptime target: 99.5% monthly for Phase 1 MVP *(default — confirm with engineering)*.
- Recovery Time Objective (RTO): 4 hours *(default — confirm with engineering)*.
- Recovery Point Objective (RPO): 15 minutes *(default — confirm with engineering)*.

### Scalability
- Architecture must support horizontal scaling for API and web layers without code redesign.
- Data layer must support at least 50,000 idea records without material degradation in list/detail retrieval p95 latency *(default — confirm with engineering)*.

### Accessibility
- UI must conform to WCAG 2.1 AA for keyboard navigation, color contrast, and semantic labeling.

### Compliance
- Platform must align with EPAM internal security/privacy standards and enterprise audit requirements *(assumed — validate with compliance team)*.

---

## 6. Success Metrics

> How we measure whether this product/feature is successful.

| Metric                    | Baseline       | Target         | Measurement Method          |
|---------------------------|----------------|----------------|-----------------------------|
| Monthly active submitters creating at least one idea | 80 users/month *(assumed — validate with current program data)* | 100 users/month within 6 months (+25%) | Product analytics events: `idea_submitted` by distinct user ID, monthly rollup |
| Median submission-to-decision cycle time | 14 days *(assumed — validate with historical workflow data)* | 8.4 days within 3 months (-40%) | Workflow timestamps from status audit log (`Submitted` to final decision) |
| Admin manual follow-up messages per idea | 2.0 messages/idea *(assumed — validate with communication logs)* | ≤1.0 message/idea within 3 months (-50%) | Sampled admin activity reports + tagged communication exports |
| API reliability for authenticated endpoints | 97.5% successful requests *(default — confirm with engineering)* | ≥99.0% successful requests per month | API monitoring dashboards (HTTP success/error ratios) |
| Defect leakage to production (P1/P2) in MVP modules | 6 defects/release *(assumed — validate with QA history)* | ≤2 defects/release by second post-launch release | QA defect tracking and production incident logs |

---

## 7. Scope

### In Scope
- JWT-based authentication, registration, and role-based authorization for `Submitter` and `Admin`.
- Structured idea submission with title, description, category, and single-file attachment.
- Idea listing and detail views with transparent status visibility and evaluator comments.
- Admin evaluation workflow for status transitions (`Submitted`, `Under Review`, `Accepted`, `Rejected`).
- Admin ability to reopen previously `Accepted` or `Rejected` ideas back to `Under Review` with reason capture.
- Core auditability for status changes and evaluator comments.

### Out of Scope
- Multi-stage committee workflows beyond basic admin accept/reject decisioning.
- Multi-file attachments, rich media processing, or large-file content management integrations.
- External-facing idea submissions from non-employees or guest users.
- Anonymous/blinded evaluation.
- Advanced AI features (automatic scoring, clustering, summarization, recommendation ranking) in Phase 1 MVP.
- Portfolio-level funding, budgeting, or implementation project tracking after acceptance.

### Future Considerations
- AI-assisted idea deduplication, semantic tagging, and evaluator recommendation support.
- Integration with enterprise collaboration tools (e.g., Teams/Jira/Confluence) for downstream execution tracking.
- Configurable evaluation rubrics and multi-reviewer approval chains.

---

## Appendix

### Assumptions
- Current fragmented process relies primarily on email/spreadsheet workflows and lacks reliable status transparency.
- Historical baseline metrics (participation, cycle time, follow-up volume, defects) are not currently centralized and require data validation.
- All users are EPAM employees with corporate identity access for authentication.
- Rejected ideas require evaluator comments for clarity and fairness *(assumed policy — validate with stakeholders)*.
- Phase 1 MVP is internal-only and targets one primary business unit before broader rollout *(assumed — validate rollout plan)*.

### Dependencies
- Availability of corporate identity/auth integration compatible with JWT-based backend.
- Deployment readiness of Next.js/React frontend and FastAPI backend environments.
- File storage capability for secure single-file attachments with access controls.
- Analytics/monitoring stack to track product usage, workflow timing, and API reliability.
- QA automation framework and CI pipeline capable of enforcing 80%+ coverage gates.

### Open Questions
- [ ] Which exact business units are included in the first rollout cohort and success baseline?

### Revision History

| Version | Date       | Author          | Summary of Changes |
|---------|------------|-----------------|-------------------|
| 1.0     | 2026-02-24 | GitHub Copilot | Initial draft     |
