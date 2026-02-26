# User Story: View Audit History

**Story ID:** US-04.04
**Parent Epic:** EPIC-04 — Admin Evaluation and Audit Workflow
**Author:** GitHub Copilot
**Status:** Backlog
**Sprint / Iteration:** TBD
**Last Updated:** 2026-02-24

---

## 1. User Story

> As a **Elif, the Innovation Program Manager**,
> I want **to view a timestamped history of status changes and evaluator comments for an idea**,
> so that **I can verify decision traceability and explain outcomes clearly**.

---

## 2. Acceptance Criteria

- [ ] **AC-1:** Given an authenticated Admin and an idea with workflow history, when the admin opens audit history, then events are shown in chronological order with timestamp, actor, and action.
- [ ] **AC-2:** Given a status change event, when it appears in the history list, then both previous and new status values are displayed.
- [ ] **AC-3:** Given a reopen event, when it appears in the history list, then the reopen reason is displayed.
- [ ] **AC-4:** Given an idea with no recorded events, when audit history is opened, then the UI displays a clear empty-state message and no system error.

---

## 3. Technical Notes

- **Approach / Constraints:** Audit history must include status changes, comments, and reopen actions with timestamps.
- **API / Integrations:** Reads from existing workflow audit log source.
- **Data / Schema:** Event data includes actor, timestamp, action type, and relevant payload (status/comment/reopen reason).
- **Edge Cases:** Empty history state.
- **Design Assets:** No technical constraints identified at this stage.

---

## 4. Estimation

**Story Points:** 3

**Estimated Days:** 2 days

**Confidence:** Medium

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

- [ ] Confirm whether submitters should see full audit event actor details or only admin comments in MVP.
