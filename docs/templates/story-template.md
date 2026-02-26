# User Story: [SHORT TITLE]

<!-- Naming convention: Use a short, action-oriented title describing what the user can do.
     e.g., "Reset Password via Email", "Filter Search Results by Date", "Export Report as PDF" -->

**Story ID:** [US-XXX]
**Parent Epic:** [EPIC-XXX — Link or title of the parent epic]
**Author:** [AUTHOR NAME]
**Status:** [Backlog | Ready | In Progress | In Review | Done]
**Sprint / Iteration:** [Sprint X or TBD]
**Last Updated:** [YYYY-MM-DD]

---

## 1. User Story

<!-- Follow the canonical format exactly. All three parts are required.
     - "As a [persona]"  → who is performing the action (use a defined persona, not a job title)
     - "I want [action]" → the specific capability or behaviour they want
     - "so that [benefit]" → the outcome or value they receive (the "why") -->

> As a **[PERSONA]**,
> I want **[ACTION / CAPABILITY]**,
> so that **[BENEFIT / OUTCOME]**.

---

## 2. Acceptance Criteria

<!-- Write 3–5 criteria that define exactly when this story is "done".
     Use Given / When / Then (Gherkin) format for clarity and testability.
     Every criterion must be independently verifiable by a tester or reviewer.
     Avoid vague language like "works correctly" or "loads fast". -->

- [ ] **AC-1:** Given [PRECONDITION], when [ACTION], then [EXPECTED OUTCOME].
- [ ] **AC-2:** Given [PRECONDITION], when [ACTION], then [EXPECTED OUTCOME].
- [ ] **AC-3:** Given [PRECONDITION], when [ACTION], then [EXPECTED OUTCOME].
- [ ] **AC-4:** Given [PRECONDITION], when [ACTION], then [EXPECTED OUTCOME]. *(optional)*
- [ ] **AC-5:** Given [PRECONDITION], when [ACTION], then [EXPECTED OUTCOME]. *(optional)*

---

## 3. Technical Notes

<!-- Optional — fill in only when there is meaningful implementation context.
     Use this for: known constraints, suggested approach, API contracts, data model notes,
     performance requirements, or links to designs/diagrams.
     This section should inform engineers, not prescribe a solution. -->

- **Approach / Constraints:** [Any known technical constraints or a preferred approach, if already decided]
- **API / Integrations:** [Relevant endpoints, third-party services, or internal services involved]
- **Data / Schema:** [Fields, models, or database changes required]
- **Edge Cases:** [Known edge cases the implementation must handle]
- **Design Assets:** [Link to Figma / wireframes / mockups, if applicable]

---

## 4. Estimation

<!-- Choose ONE estimation method (story points or days) and use it consistently across the team.
     Story points measure complexity + uncertainty, not time.
     If splitting is needed, a story estimated above 8 points should typically be broken down. -->

**Story Points:** [1 / 2 / 3 / 5 / 8 / 13]
<!-- Common scale: 1=trivial, 2=simple, 3=small, 5=medium, 8=large, 13=needs splitting -->

**Estimated Days:** [X days] *(optional, use only if the team works in days instead of points)*

**Confidence:** [High / Medium / Low]
<!-- Low confidence = unknowns remain; consider a spike story before committing -->

---

## INVEST Checklist

<!--
Use this checklist during backlog refinement to validate the story before it enters a sprint.
All boxes should be checked before marking a story as "Ready".

[ ] INDEPENDENT  — This story can be developed and delivered without being blocked by another
                   story. Dependencies on infrastructure or epics are acceptable; story-to-story
                   dependencies should be minimised.

[ ] NEGOTIABLE   — The details of implementation are open for discussion between the team
                   and stakeholders. The story is not a rigid specification.

[ ] VALUABLE     — The story delivers clear, direct value to the persona or the business.
                   If the value is only internal (e.g., refactoring), make that explicit.

[ ] ESTIMABLE    — The team has enough information to estimate the effort. If not, create a
                   spike story to resolve the unknowns first.

[ ] SMALL        — The story can be completed within a single sprint. If it cannot, split it
                   into smaller stories, each independently valuable.

[ ] TESTABLE     — Each acceptance criterion can be verified by a tester without ambiguity.
                   If you cannot write a test for it, rewrite the criterion.
-->

- [ ] **Independent** — Can be built and shipped without depending on another unfinished story
- [ ] **Negotiable** — Implementation details are open; the story captures intent, not a spec
- [ ] **Valuable** — Delivers clear value to the persona or business on its own
- [ ] **Estimable** — Team has enough context to size this story confidently
- [ ] **Small** — Completable within one sprint; split if estimated above 8 points
- [ ] **Testable** — Every acceptance criterion is specific and independently verifiable

---

## Notes & Open Questions

<!-- Capture anything unresolved that must be answered before the story can move to "Ready". -->

- [ ] [OPEN QUESTION 1 — e.g., Should validation happen client-side, server-side, or both?]
- [ ] [OPEN QUESTION 2]
