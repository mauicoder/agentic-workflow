---
name: to-tickets
description: >-
  Break a specification, plan, or conversation into dependency-graphed tracer-bullet
  tickets with explicit blocking edges, saved to docs/tickets/<feature-slug>/ (or
  published to the configured issue tracker). Use when the user asks to slice a spec
  into tickets, run /to-tickets, or generate a task dependency graph.
---

# To Tickets

Break a specification, plan, or conversation into a set of **tickets**: tracer-bullet vertical slices, each declaring the tickets that **block** it.

## Tracker & Storage Resolution

Check `.agents/workflows/agentic-tdd-sdlc.yaml` if present, or follow the user's explicit instruction:
- **Phase Model:** `"Gemini 4 Argon"` (`models.ticketization`) — pass `model="Gemini 4 Argon"` explicitly when invoking ticketization/architecture slicing agents via `run_workflow` or `invoke_subagent`.
- **Local mode (default):** Write one file per ticket under `docs/tickets/<feature-slug>/<NN>-<ticket-slug>.md`, numbered from `01` in dependency order (blockers first).
- **External tracker (`github`, `gitlab`, `linear`):** Publish one issue per ticket in dependency order and wire native blocking relationships (or list blockers in `Blocked by`). Apply the `ready-for-agent` label.

## Process

### 1. Gather context

Locate the active specification:
1. A spec path, issue number, or URL passed by the user.
2. The most recent spec under `docs/specs/`.
3. The current conversation context.

### 2. Explore the codebase (if needed)

If you have not yet explored the codebase, inspect the relevant areas so ticket titles and descriptions use the project's domain vocabulary and respect existing ADRs.

Look for opportunities to **prefactor** the code or define shared interface contracts first ("Make the change easy, then make the easy change").

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but **complete** path through every required layer (contract/schema, domain logic, API/UI, tests): vertical, **not** a horizontal slice of one layer.
- If multiple modules must be built in parallel, create a root contract/prefactor ticket first so downstream vertical slices can be developed concurrently against stable interfaces.
- A completed slice is verifiable and passes tests on its own.
- Each slice is sized to fit comfortably in a single subagent context window.

</vertical-slice-rules>

Assign each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers (`None (can start immediately)`) is on the initial frontier.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change (renaming a column, retyping a shared symbol) whose blast radius fans across the codebase so no vertical slice can land green alone. Sequence wide refactors as **expand → migrate → contract**:
1. **Expand:** Add the new form alongside the old so nothing breaks.
2. **Migrate:** Migrate call sites in batches sized by blast radius (per package/directory), each batch its own ticket blocked by the expand ticket, keeping tests green after every batch.
3. **Contract:** Remove the old form in a final ticket blocked by all migrate tickets.

### 4. Confirm the breakdown with the user

Present the proposed ticket graph as a numbered list showing for each ticket:
- **Title:** Short descriptive name
- **Blocked by:** Which other tickets (if any) must complete first
- **What it delivers:** The end-to-end behavior or contract this ticket establishes

Ask the user to confirm:
- Does the granularity feel right?
- Are the blocking edges minimal and accurate?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 5. Publish the tickets

Write the approved tickets in dependency order (blockers first):

- **Local files (default):** Write one file per ticket under `docs/tickets/<feature-slug>/<NN>-<ticket-slug>.md` (e.g., `docs/tickets/auth-flow/01-session-contract.md`). Never combine multiple tickets into a single file.
- **External tracker:** Publish one issue per ticket in dependency order, link parent/sub-issues and blocking edges, and apply the `ready-for-agent` label. Do **not** close or overwrite the parent spec issue.

<local-ticket-template>

# <NN>: <Ticket title>

**Spec:** `docs/specs/<feature-slug>.md`

**What to build:** The end-to-end behavior or contract this ticket makes work, from the caller's or user's perspective rather than a file-by-file checklist.

**Blocked by:** `<NN>-<slug>` (or `None (can start immediately)`)

**Status:** ready-for-agent

## Acceptance Criteria

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent spec issue on the tracker (omit if none).

## What to build

The end-to-end behavior this ticket makes work, from the user's perspective, not layer-by-layer implementation.

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Blocked by

- Reference to each blocking ticket, or `None (can start immediately)`.

</issue-template>

Avoid brittle file paths or large code snippets unless a concise type/contract excerpt from a prototype captures an interface decision more accurately than prose.
