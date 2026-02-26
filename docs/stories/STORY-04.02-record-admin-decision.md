# User Story: Record Admin Decision

**Story ID:** US-04.02
**Parent Epic:** EPIC-04 — Admin Evaluation and Audit Workflow
**Author:** GitHub Copilot
**Status:** Backlog
**Sprint / Iteration:** TBD
**Last Updated:** 2026-02-24

---

## 1. User Story

> As a **Elif, the Innovation Program Manager**,
> I want **to mark an idea as Accepted or Rejected with decision comments**,
> so that **submitters receive clear outcomes and decisions are traceable**.

---

## 2. Acceptance Criteria

- [ ] **AC-1:** Given an authenticated Admin and an idea in `Under Review`, when the admin selects `Accepted` with optional comment, then the decision is saved and visible on idea details.
- [ ] **AC-2:** Given an authenticated Admin and an idea in `Under Review`, when the admin selects `Rejected` without comment, then the system blocks submission and displays “Rejection comment is required.”
- [ ] **AC-3:** Given an authenticated Admin and an idea in `Under Review`, when the admin selects `Rejected` with comment text, then the decision and comment are saved successfully.
- [ ] **AC-4:** Given a decision save failure (for example transient backend error), when the admin submits the decision, then the UI shows an error and keeps the idea in its prior status.

---

## 3. Technical Notes

- **Approach / Constraints:** Rejected decisions require comments per PRD policy.
- **API / Integrations:** Uses admin decision workflow endpoints and existing authenticated API layer.
- **Data / Schema:** Persist final status and evaluator comment; include timestamps in audit trail.
- **Edge Cases:** Rejection without comment; backend save failure.
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

- None.
