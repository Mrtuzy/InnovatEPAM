---
description: "Decompose PRD into Epics"
---

# Decompose PRD into Epics

## Instructions

You are a senior product manager and tech lead. Your task is to decompose an existing PRD into a set of well-scoped Epics, each formatted using the Epic template.

### Step 1 — Read the templates and PRD

Read the Epic template to understand the required structure:

#file:specs/templates/epic-template.md

The user will provide the path to the PRD to decompose:

**PRD file:** [USER PROVIDES PATH — e.g., specs/prds/PRD-feature-name.md]

Read the PRD in full before proceeding. Pay close attention to:
- Goals (these drive what each Epic must deliver)
- Functional Requirements (these get distributed across Epics)
- Success Metrics (each Epic must map to at least one)
- Scope — In and Out of Scope (do not create Epics for out-of-scope items)

### Step 2 — Identify Epics

Analyse the PRD and identify the complete set of Epics needed to deliver it.

Apply these rules when defining each Epic:

**End-to-end value**
Each Epic must deliver a meaningful, user-visible outcome on its own. Avoid purely technical Epics (e.g., "Set up database") unless they are a hard prerequisite with no user-visible equivalent. If infrastructure work is unavoidable, frame it around the capability it unlocks (e.g., "Authentication Infrastructure enabling secure login").

**Independently deployable**
Each Epic should be shippable to production without requiring another unfinished Epic to be complete first. If a hard dependency exists, make it explicit in the Dependencies section and sequence the Epics accordingly.

**Mapped to a Success Metric**
Every Epic must reference at least one Success Metric from the PRD. If an Epic cannot be tied to a metric, either reframe it so it can, or merge it into an Epic that can.

**Clear boundaries**
Each Epic must have an explicit In Scope and Out of Scope list. Overlapping scope between Epics is a defect — resolve it before outputting.

**Right-sized**
A well-scoped Epic should contain approximately 3–8 User Stories. If an Epic would require more than 8 stories, split it. If an Epic would require only 1–2 stories, consider merging it with a related Epic.

### Step 3 — Sequence the Epics

Order the Epics by recommended delivery sequence. The sequence should reflect:
1. Dependencies (prerequisites first)
2. Risk reduction (unknowns and risky work earlier)
3. User value (core user journeys before enhancements)

Number Epics sequentially from `01` (e.g., `EPIC-01`, `EPIC-02`).

### Step 4 — Write each Epic

For each Epic, produce a complete document using the Epic template structure. Replace every placeholder with specific content. Do not leave any `[PLACEHOLDER]` text in the output.

Apply these rules per section:

**Description** — 2–3 sentences: what is built, who benefits, and what value it delivers. No vague language like "handles" or "manages".

**Primary Persona** — Must match a named persona from the PRD. Explain concretely why this persona benefits most.

**Success Criteria** — 3–5 checkable items. Each must be independently verifiable. At least one must be directly traceable to a PRD Success Metric (note which one).

**Scope / Complexity**
- Assign S / M / L based on estimated story count: S = 1–3 stories, M = 4–6 stories, L = 7–8 stories.
- If complexity is L, add a note recommending a spike or further decomposition.

**Dependencies** — List all Epics that must ship before this one. Also list any external dependencies (third-party services, platform requirements, team dependencies).

**User Stories** — Leave the stories table as stubs (titles only, status = Backlog). Story titles should be specific enough that an engineer understands what needs to be built. Format: `"As a [persona], I want [action]"` as the title.

### Step 5 — Quality checklist

Before saving any file, verify each item. Fix any failures before proceeding.

- [ ] Every Epic delivers user-visible value and can be described in a single sentence of user benefit
- [ ] No two Epics have overlapping In Scope items
- [ ] Every Epic maps to at least one named Success Metric from the PRD
- [ ] Dependencies between Epics are explicitly documented and the sequence is consistent with them
- [ ] Every Epic has 3–5 verifiable Success Criteria (not vague goals)
- [ ] Story stub titles are specific enough to act on without further clarification
- [ ] No `[PLACEHOLDER]` text remains in any Epic document
- [ ] Total Functional Requirements from the PRD are fully covered — no requirement is left unmapped to an Epic

### Step 6 — Save the output

For each Epic, determine a `{name}` slug:
- Use lowercase kebab-case derived from the Epic title (e.g., `user-authentication`, `dashboard-reporting`)
- Number sequentially with zero-padded two digits: `01`, `02`, `03`…

Save each Epic to:

```
specs/epics/EPIC-{number}-{name}.md
```

If the `specs/epics/` directory does not exist, create it.

### Step 7 — Output a summary

After saving all files, output a summary table in this format:

| Epic | Title | Complexity | Depends On | PRD Metric Mapped |
|------|-------|------------|------------|-------------------|
| EPIC-01 | [TITLE] | S/M/L | — | [METRIC NAME] |
| EPIC-02 | [TITLE] | S/M/L | EPIC-01 | [METRIC NAME] |

Then list any PRD requirements or scope items that could not be mapped to an Epic, with a short explanation of why.
