# Epic: Admin Evaluation and Audit Workflow

**Epic ID:** EPIC-04
**Related PRD:** specs/prds/PRD-innovatepam-portal.md
**Author:** GitHub Copilot
**Status:** Backlog
**Target Release:** MVP Wave 2
**Last Updated:** 2026-02-24

---

## 1. Description

This epic enables admins to move ideas through evaluation states, capture decision comments, reopen closed ideas when needed, and maintain an auditable workflow trail. It gives innovation managers a controlled process from initial review to final outcome while preserving transparency for submitters and stakeholders. The business value is faster, more consistent decisions with lower operational rework.

---

## 2. Primary Persona

**Persona:** Elif, the Innovation Program Manager

**Why they benefit:** Elif is responsible for fair and timely decisions and needs structured state transitions, comment capture, and historical traceability. Reopen capability supports correction and reconsideration without off-platform workarounds.

---

## 3. Success Criteria

- [ ] Admins can transition ideas through Submitted, Under Review, Accepted, and Rejected according to workflow rules.
- [ ] Rejected decisions require comments, and reopening an Accepted or Rejected idea requires a mandatory reopen reason.
- [ ] Median submission-to-decision cycle time improves from baseline 14 days to target 8.4 days within 3 months (traceable to PRD metric: Median submission-to-decision cycle time).
- [ ] Every status change, comment, and reopen action is captured in immutable timestamped audit history.
- [ ] No critical workflow integrity defects remain open at release readiness.

---

## 4. Scope / Complexity

**Estimate:** L

**Justification:** This epic includes workflow rule enforcement, role-protected state changes, audit integrity, and edge-case handling for reopen behavior across API and UI.

### In Scope
- Admin workflow actions for status transitions and decision comments.
- Reopen action from Accepted or Rejected back to Under Review with mandatory reason.
- Timestamped audit trail for status changes and evaluator comments.
- Workflow integrity tests and release-readiness acceptance checks.

### Out of Scope
- Multi-stage committee approvals or weighted scoring matrices.
- Anonymous/blinded evaluation.
- Budget allocation and implementation project execution post-acceptance.

---

## 5. Dependencies

| Dependency                          | Type                          | Status              | Owner / Notes                  |
|-------------------------------------|-------------------------------|---------------------|-------------------------------|
| EPIC-01 Secure Access and Role Control | Technical | Pending | Required for admin-only workflow actions |
| EPIC-02 Idea Submission and Attachment Intake | Technical | Pending | Requires submitted ideas to evaluate |
| EPIC-03 Idea Visibility and Status Tracking | Technical | Pending | Shares detail surfaces for comments and history |
| Policy confirmation for reopen governance | Design | Pending | Product and program governance decision needed |

---

## 6. User Stories

> ⚠️ Stories have not been written yet. This section will be populated during sprint planning or backlog refinement.

| Story ID   | Title                          | Status              |
|------------|--------------------------------|---------------------|
| US-04.01   | Start Admin Review | Backlog |
| US-04.02   | Record Admin Decision | Backlog |
| US-04.03   | Reopen Closed Idea | Backlog |
| US-04.04   | View Audit History | Backlog |
| US-04.05   | Enforce Workflow Integrity Rules | Backlog |
| US-04.06   | Track Evaluation Cycle Time | Backlog |

---

## Notes & Open Questions

- [ ] Confirm whether reopen action should notify submitter immediately in MVP.
- [ ] Confirm SLA expectation for first admin review after submission.
- [ ] L complexity: recommend a short spike to validate transition model and audit schema before full implementation.
