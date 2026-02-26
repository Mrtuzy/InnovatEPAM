# User Story: Start Admin Review

**Story ID:** US-04.01
**Parent Epic:** EPIC-04 — Admin Evaluation and Audit Workflow
**Author:** GitHub Copilot
**Status:** Backlog
**Sprint / Iteration:** TBD
**Last Updated:** 2026-02-24

---

## 1. User Story

> As a **Elif, the Innovation Program Manager**,
> I want **to move an idea from Submitted to Under Review**,
> so that **I can begin structured evaluation without off-platform coordination**.

---

## 2. Acceptance Criteria

- [ ] **AC-1:** Given an authenticated Admin and an idea in `Submitted`, when the admin selects `Under Review`, then the idea status is updated to `Under Review` and persisted.
- [ ] **AC-2:** Given a non-admin user, when they attempt to call the status-change action, then the system returns authorization denied and no status change is saved.
- [ ] **AC-3:** Given an idea already in `Accepted` or `Rejected`, when an admin attempts a direct transition to `Under Review` through the standard transition action, then the system rejects it and instructs using the reopen action.
- [ ] **AC-4:** Given a successful status update, when the update completes, then a timestamped audit event is created with actor, previous status, and new status.

---

## 3. Technical Notes

- **Approach / Constraints:** Admin-only workflow action; allowed transition in this story is `Submitted` → `Under Review`.
- **API / Integrations:** Uses authenticated admin workflow endpoints defined in EPIC-04 scope.
- **Data / Schema:** Status values include `Submitted`, `Under Review`, `Accepted`, `Rejected`; audit event includes timestamp and actor.
- **Edge Cases:** Unauthorized actor attempt; invalid state transition.
- **Design Assets:** No technical constraints identified at this stage.

---

## 4. Estimation

**Story Points:** 3

**Estimated Days:** 2 days

**Confidence:** High

---

## INVEST Checklist

- [x] **Independent** — Can be built and shipped without depending on another unfinished story
- [x] **Negotiable** — Implementation details are open; the story captures intent, not a spec
- [x] **Valuable** — Delivers clear value to the persona or business on its own
- [x] **Estimable** — Team has enough context to size this story confidently
- [x] **Small** — Completable within one sprint; split if estimated above 8 points
- [x] **Testable** — Every acceptance criterion is specific and independently verifiable

---

## Notes & Open Questions

- None.
