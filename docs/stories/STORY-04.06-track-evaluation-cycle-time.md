# User Story: Track Evaluation Cycle Time

**Story ID:** US-04.06
**Parent Epic:** EPIC-04 — Admin Evaluation and Audit Workflow
**Author:** GitHub Copilot
**Status:** Backlog
**Sprint / Iteration:** TBD
**Last Updated:** 2026-02-24

---

## 1. User Story

> As a **Elif, the Innovation Program Manager**,
> I want **to view median submission-to-decision cycle time from workflow timestamps**,
> so that **I can monitor whether evaluation speed is improving against the target**.

---

## 2. Acceptance Criteria

- [ ] **AC-1:** Given ideas with both `Submitted` and final decision timestamps, when cycle-time reporting is generated, then median submission-to-decision duration is calculated from those timestamps.
- [ ] **AC-2:** Given ideas without a final decision timestamp, when cycle-time reporting runs, then those ideas are excluded from median calculation and counted as in-progress.
- [ ] **AC-3:** Given data quality issues (for example missing `Submitted` timestamp), when reporting runs, then affected records are excluded and surfaced in a data-quality warning output.
- [ ] **AC-4:** Given a reporting period, when results are displayed, then baseline 14 days and target 8.4 days are shown alongside current median for comparison.

---

## 3. Technical Notes

- **Approach / Constraints:** Metric is defined in PRD as median submission-to-decision cycle time from workflow audit timestamps.
- **API / Integrations:** Reads workflow timestamps from audit/history data used by the evaluation system.
- **Data / Schema:** Requires `Submitted` event timestamp and terminal decision event timestamp.
- **Edge Cases:** In-progress ideas and missing timestamp records must not corrupt median.
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

- [ ] Confirm reporting cadence (daily/weekly/monthly) for MVP dashboard views.
