# Epic: Idea Submission and Attachment Intake

**Epic ID:** EPIC-02
**Related PRD:** specs/prds/PRD-innovatepam-portal.md
**Author:** GitHub Copilot
**Status:** Backlog
**Target Release:** MVP Wave 1
**Last Updated:** 2026-02-24

---

## 1. Description

This epic delivers the submitter-facing flow for creating innovation ideas using a structured form and one supporting attachment. It gives employees a consistent channel to provide complete, evaluable submissions instead of fragmented email or spreadsheet inputs. The result is higher-quality idea intake and measurable growth in program adoption.

---

## 2. Primary Persona

**Persona:** Deniz, the Employee Submitter

**Why they benefit:** Deniz needs a clear, standardized submission path that captures required details and supporting evidence in one place. This epic removes ambiguity and reduces friction in getting ideas into review.

---

## 3. Success Criteria

- [ ] Submitters can create an idea with required title, description, and category fields, and invalid payloads are rejected with actionable errors.
- [ ] Single-file attachment upload supports approved size/type limits and blocks invalid files with explicit feedback.
- [ ] Monthly active submitters creating at least one idea increases from baseline 80 to target 100 within 6 months (traceable to PRD metric: Monthly active submitters creating at least one idea).
- [ ] Submission API and UI flows are covered by automated tests aligned with MVP quality gates.

---

## 4. Scope / Complexity

**Estimate:** M

**Justification:** The epic combines form UX, validation, file handling, API integration, and error-state behavior that must work consistently across client and server.

### In Scope
- Structured idea submission form with required fields and category selection.
- Single-file upload with type and size validation (allowed: `pdf`, `png`, `jpg`, `jpeg`; max 10MB).
- Submission confirmation and persisted Submitted status initialization.
- Submission-specific automated testing and validation checks.

### Out of Scope
- Multi-file upload or rich media handling.
- AI-generated content suggestions during submission.
- Advanced draft/versioning workflow.

---

## 5. Dependencies

| Dependency                          | Type                          | Status              | Owner / Notes                  |
|-------------------------------------|-------------------------------|---------------------|-------------------------------|
| EPIC-01 Secure Access and Role Control | Technical | Pending | Requires authenticated submitter sessions |
| File storage service for attachments | Technical | Pending | Backend and infrastructure setup required |
| Attachment validation implementation (`pdf`, `png`, `jpg`, `jpeg`; max 10MB) | Technical | Pending | Frontend and backend validation must match |

---

## 6. User Stories

> ⚠️ Stories have not been written yet. This section will be populated during sprint planning or backlog refinement.

| Story ID   | Title                          | Status              |
|------------|--------------------------------|---------------------|
| US-201   | As a submitter, I want to create an idea with title, description, and category so it can be evaluated | Backlog |
| US-202   | As a submitter, I want to upload one supporting file so evaluators can review context | Backlog |
| US-203   | As a submitter, I want clear validation messages when required fields are missing so I can correct quickly | Backlog |
| US-204   | As a submitter, I want invalid attachment types or sizes rejected with guidance so I can resubmit correctly | Backlog |
| US-205   | As a product analyst, I want submission events instrumented so adoption metrics can be measured reliably | Backlog |

---

## Notes & Open Questions

- [ ] Confirm whether duplicate idea warning is needed in MVP or deferred.
