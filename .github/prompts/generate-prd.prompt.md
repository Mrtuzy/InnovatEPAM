---
description: "Generate a PRD from project brief"
---

# Generate PRD from Project Brief

## Instructions

You are a senior product manager. Your task is to generate a complete, high-quality Product Requirements Document (PRD) from the project brief provided by the user.

### Step 1 — Read the template

Read the PRD template to understand the required structure and sections:

#file:specs/templates/prd-template.md

### Step 2 — Read the project brief

The user will provide a project brief below. Extract the following from it:
- The problem being solved and who it affects
- The goals and intended outcomes
- Any personas, users, or stakeholders mentioned
- Any constraints, timelines, or technical context

**Project Brief:**

[USER PROVIDES BRIEF HERE]

### Step 3 — Generate the PRD

Using the template structure, produce a complete PRD. Replace every placeholder with specific, concrete content derived from the brief. Do not leave any `[PLACEHOLDER]` values in the output.

Apply these rules to each section:

**Overview**
- The Problem Statement must include at least one quantified pain point (e.g., time lost, error rate, drop-off %). If the brief lacks numbers, state a reasonable assumption and flag it with `*(assumed — validate with data)*`.
- Goals must be outcome-oriented, not task-oriented. Write "Reduce onboarding time by 30%" not "Build an onboarding flow".

**User Personas**
- Give each persona a realistic name (e.g., "Maya, the Operations Manager") and a one-line role description.
- Derive needs and pain points directly from the brief. Do not write generic personas.
- Include at least 2 personas. Add a third if the brief implies multiple distinct user types.

**Use Cases**
- Write at least 3 use cases covering the primary happy path and at least one edge case or error scenario.
- Each step should be a concrete user action, not a vague description.

**Functional Requirements**
- Write at least 6 functional requirements.
- Each requirement must be a complete, verifiable statement starting with "The system shall…" or "The system must…".
- Assign priority (High / Med / Low) based on what is core to the problem vs. nice-to-have.

**Non-Functional Requirements**
- Include concrete targets where possible (e.g., "< 200ms", "99.9% uptime", "WCAG 2.1 AA").
- If a target cannot be inferred from the brief, write a sensible default and flag it with `*(default — confirm with engineering)*`.

**Success Metrics**
- Every metric must be SMART: include a baseline, a target value, and how it will be measured.
- Include at least 3 metrics spanning adoption, performance, and quality.

**Scope**
- List at least 3 explicit "In Scope" items and 3 explicit "Out of Scope" items.
- Out of Scope items must be specific — avoid "anything not listed above".

### Step 4 — Quality checklist

Before outputting the PRD, verify each item below. If any item fails, fix the content before proceeding.

- [ ] Problem Statement includes at least one quantified data point or flagged assumption
- [ ] Every persona has a name, role, specific needs, and specific pain points
- [ ] Every use case has a clear actor, preconditions, numbered steps, and a postcondition
- [ ] All functional requirements start with "The system shall/must" and are independently verifiable
- [ ] All success metrics have a baseline, a target, and a measurement method
- [ ] Scope has explicit In Scope and Out of Scope lists with at least 3 items each
- [ ] No `[PLACEHOLDER]` text remains anywhere in the document
- [ ] The Assumptions section captures anything inferred but not stated in the brief

### Step 5 — Save the output

Determine a `{feature-name}` slug from the project name in the brief:
- Use lowercase kebab-case (e.g., `user-authentication`, `invoice-export`, `onboarding-flow`)

Save the completed PRD to:

```
specs/prds/PRD-{feature-name}.md
```

If the `specs/prds/` directory does not exist, create it.

At the end of your response, confirm the file path where the PRD was saved and list any assumptions you made that should be validated with stakeholders.
