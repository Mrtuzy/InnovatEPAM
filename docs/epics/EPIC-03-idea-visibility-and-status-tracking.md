# Epic: Idea Visibility and Status Tracking

**Epic ID:** EPIC-03
**Related PRD:** specs/prds/PRD-innovatepam-portal.md
**Author:** GitHub Copilot
**Status:** Backlog
**Target Release:** MVP Wave 2
**Last Updated:** 2026-02-24

---

## 1. Description

This epic provides transparent idea list and detail experiences so users can monitor progress without manual follow-up. Submitters can view current status, last update timestamps, and evaluator comments for their own ideas, while admins can browse all ideas for operational visibility. This directly reduces coordination overhead and improves trust in the innovation pipeline.

---

## 2. Primary Persona

**Persona:** Deniz, the Employee Submitter

**Why they benefit:** Deniz currently lacks visibility after submission and must chase updates manually. This epic gives continuous self-service status tracking and comment visibility.

---

## 3. Success Criteria

- [ ] Submitters can access a My Ideas view showing only their own ideas with current status and last updated timestamp.
- [ ] Admins can access an all-ideas list and open details for any idea under evaluation.
- [ ] At least 90% of status lookup actions are completed through portal views rather than manual follow-up channels within 3 months (traceable to PRD metric: Admin manual follow-up messages per idea).
- [ ] List and detail APIs meet p95 response targets under expected MVP load.

---

## 4. Scope / Complexity

**Estimate:** M

**Justification:** This epic covers role-filtered read access, list/detail data presentation, and performance-sensitive retrieval behavior.

### In Scope
- Role-aware idea listing screens for submitters and admins.
- Idea detail pages with status timeline context and evaluator comments.
- Last updated timestamps and basic filtering/sorting needed for operational use.
- Observability for status-view usage and response-time monitoring.

### Out of Scope
- Bulk edit or workflow state change actions.
- Portfolio analytics dashboards and executive reporting.
- External notifications (email/chat) for status changes.

---

## 5. Dependencies

| Dependency                          | Type                          | Status              | Owner / Notes                  |
|-------------------------------------|-------------------------------|---------------------|-------------------------------|
| EPIC-01 Secure Access and Role Control | Technical | Pending | Needed for role-aware visibility |
| EPIC-02 Idea Submission and Attachment Intake | Technical | Pending | Requires idea data to display |
| Monitoring instrumentation standards | External | Pending | Observability team alignment needed |

---

## 6. User Stories

> ⚠️ Stories have not been written yet. This section will be populated during sprint planning or backlog refinement.

| Story ID   | Title                          | Status              |
|------------|--------------------------------|---------------------|
| US-301   | As a submitter, I want to view my idea list with current statuses so I can track progress | Backlog |
| US-302   | As a submitter, I want to open idea details and read evaluator comments so I understand outcomes | Backlog |
| US-303   | As an admin, I want to view all ideas with status filters so I can prioritize review workload | Backlog |
| US-304   | As a user, I want to see the last updated timestamp so I can understand recency of decisions | Backlog |
| US-305   | As an operations analyst, I want view-usage metrics so reduction in manual follow-up can be measured | Backlog |

---

## Notes & Open Questions

- [ ] Confirm minimum filtering options needed for MVP list usability.
- [ ] Confirm data retention period for historical idea visibility.
