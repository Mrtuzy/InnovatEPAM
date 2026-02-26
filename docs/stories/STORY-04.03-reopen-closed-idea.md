# User Story: Reopen Closed Idea

**Story ID:** US-04.03
**Parent Epic:** EPIC-04 — Admin Evaluation and Audit Workflow
**Author:** GitHub Copilot
**Status:** Backlog
**Sprint / Iteration:** TBD
**Last Updated:** 2026-02-24

---

## 1. User Story

> As a **Elif, the Innovation Program Manager**,
> I want **to reopen an Accepted or Rejected idea back to Under Review with a required reason**,
> so that **I can correct decisions when new information appears**.

---

## 2. Acceptance Criteria

- [ ] **AC-1:** Given an authenticated Admin and an idea in `Accepted` or `Rejected`, when the admin submits a reopen reason, then the idea transitions to `Under Review`.
- [ ] **AC-2:** Given an authenticated Admin and an idea in `Accepted` or `Rejected`, when the admin attempts reopen with an empty reason, then the system blocks reopen and displays a required-field error.
- [ ] **AC-3:** Given an idea not in `Accepted` or `Rejected`, when the admin attempts reopen action, then the system denies the action and returns an invalid-state message.
- [ ] **AC-4:** Given a successful reopen, when the action is completed, then an audit event is recorded with previous status, new status, reason, actor, and timestamp.

---

## 3. Technical Notes

- **Approach / Constraints:** Reopen is permitted only from `Accepted` or `Rejected` to `Under Review` and requires a reason.
- **API / Integrations:** Uses admin-only workflow endpoint for reopen action.
- **Data / Schema:** Reopen reason must be stored and included in audit history.
- **Edge Cases:** Empty reason; reopen attempted from invalid status.
- **Design Assets:** No technical constraints identified at this stage.

---

## 4. Estimation

**Story Points:** 5

**Estimated Days:** 3 days

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

- [ ] Confirm whether reopening should trigger submitter notification in MVP.
