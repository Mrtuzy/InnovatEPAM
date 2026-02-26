---
description: "Break Epic into User Stories"
---

# Break Epic into User Stories

## Instructions

You are a senior product manager and agile practitioner. Your task is to decompose an existing Epic into a complete set of well-formed User Stories, each formatted using the Story template and validated against INVEST principles.

### Step 1 — Read the templates and Epic

Read the Story template to understand the required structure:

#file:specs/templates/story-template.md

The user will provide the path to the Epic to decompose:

**Epic file:** [USER PROVIDES PATH — e.g., specs/epics/EPIC-01-user-authentication.md]

Read the Epic in full before proceeding. Extract:
- Epic ID and title (you will use this in every Story ID)
- Primary Persona (default actor for stories unless another is more appropriate)
- Success Criteria (stories must collectively satisfy all of them)
- In Scope items (stories must stay within this boundary)
- Out of Scope items (do not write stories for these)
- User Story stubs already listed in the Epic (use as a starting point — expand, split, or merge as needed)

### Step 2 — Identify and scope the Stories

Analyse the Epic and determine the complete, minimal set of User Stories that delivers it.

Apply these rules when defining each Story:

**Coverage**
Every In Scope item from the Epic must be addressed by at least one story. Every Epic Success Criterion must be satisfiable by the stories collectively. Flag any criterion that no single story directly covers.

**Granularity**
Each story must be completable within a single sprint. If a story would require more than 5 days of work or more than one major technical concern, split it. If two stories are trivially small and always delivered together, merge them.

**Happy path before edge cases**
Write the primary happy-path story first for each capability. Then add edge case and error-handling stories as separate stories. Do not bundle happy path and error handling into one story.

**Actors**
Use the Epic's Primary Persona as the default actor. Use a different persona only when the story clearly serves a different user type — and only if that persona is defined in the parent PRD.

**Numbering**
Number stories sequentially within the Epic starting from `01` (e.g., for EPIC-03: `US-03.01`, `US-03.02`, `US-03.03`…).

### Step 3 — Write each Story

For each Story, produce a complete document using the Story template. Replace every placeholder with specific content. Do not leave any `[PLACEHOLDER]` text in the output.

Apply these rules per section:

**User Story statement**
- Must follow the exact format: `As a [persona], I want [action], so that [benefit].`
- The action must be concrete and specific — avoid vague verbs like "manage", "handle", or "use".
- The benefit must describe the user's outcome, not a system behaviour. ("so that I don't lose my work" not "so that data is saved").

**Acceptance Criteria**
- Write 3–5 criteria per story using Given / When / Then format.
- Each criterion must be independently testable by a QA engineer without ambiguity.
- Cover: the happy path (at least 1), a validation or constraint (at least 1), and an error or edge case (at least 1).
- Criteria must be specific: include exact values, states, or behaviours where possible.
- Avoid criteria that reference other stories (each story must be self-contained).

**Technical Notes**
- Include only what is known or already decided. Do not invent implementation details.
- If a relevant API, data field, or constraint is mentioned in the Epic, surface it here.
- If nothing is known yet, write: `No technical constraints identified at this stage.`

**Estimation**
- Assign story points using the Fibonacci scale: 1, 2, 3, 5, 8, 13.
- A story estimated at 13 points must be split before it enters a sprint.
- Set Confidence to Low if the story has unresolved open questions; Medium if mostly clear; High if fully understood.

**INVEST checklist**
- Complete the checklist for every story. All six items must be checked before a story is marked Ready.
- If any item cannot be checked, add an open question explaining what needs to be resolved.

### Step 4 — Quality checklist

Before saving any file, verify each item. Fix any failures before proceeding.

- [ ] Every In Scope item from the Epic is addressed by at least one story
- [ ] Every Epic Success Criterion is satisfiable by the stories collectively
- [ ] No story contains both a happy-path scenario and an unrelated error-handling scenario
- [ ] Every User Story statement uses the exact `As a / I want / so that` format with a concrete action and user-outcome benefit
- [ ] Every Acceptance Criterion uses Given / When / Then and is independently testable
- [ ] Every story covers: at least one happy-path AC, one validation AC, and one error/edge-case AC
- [ ] No story is estimated at 13 points without a note to split it
- [ ] All six INVEST criteria are checked (or have a documented open question explaining why not)
- [ ] No story references another story inside its own Acceptance Criteria
- [ ] No `[PLACEHOLDER]` text remains in any Story document

### Step 5 — Save the output

For each Story, determine a `{name}` slug:
- Use lowercase kebab-case derived from the story title (e.g., `login-with-email`, `show-validation-error`, `redirect-after-login`)
- Extract the Epic number from the Epic ID (e.g., EPIC-03 → `03`)
- Number stories sequentially with zero-padded two digits: `01`, `02`, `03`…

Save each Story to:

```
specs/stories/STORY-{epic}.{number}-{name}.md
```

Example: `specs/stories/STORY-03.01-login-with-email.md`

If the `specs/stories/` directory does not exist, create it.

### Step 6 — Update the Epic's User Stories table

After saving all Story files, update the User Stories table in the Epic file to reflect the final story list:
- Replace stub titles with the finalised story titles
- Fill in the Story ID column with the assigned IDs
- Set Status to `Backlog` for all stories

### Step 7 — Output a summary

After saving all files, output a summary table in this format:

| Story ID   | Title                        | Points | Confidence | INVEST Pass? |
|------------|------------------------------|--------|------------|--------------|
| US-XX.01   | [TITLE]                      | X      | High/Med/Low | ✅ / ⚠️ |
| US-XX.02   | [TITLE]                      | X      | High/Med/Low | ✅ / ⚠️ |

Mark INVEST as ✅ if all six criteria are checked, ⚠️ if any open questions remain.

Then list:
1. Any Epic Success Criteria not fully covered by the stories, with a recommendation
2. Any open questions that must be resolved before stories can be moved to Ready
