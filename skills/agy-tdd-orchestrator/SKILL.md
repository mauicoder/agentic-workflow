---
name: agy-tdd-orchestrator
description: >-
  Orchestrate the end-to-end multi-agent TDD software development lifecycle in
  Antigravity (agy): requirements refinement (/grill-me), specification synthesis
  (to-spec), dependency-graphed ticket slicing (to-tickets), parallel TDD execution
  (implement-spec + tdd), and two-axis verification (code-review). Use when the user
  wants to run the full TDD workflow or asks how to progress from idea to reviewed code.
---

# Antigravity TDD Multi-Agent Orchestrator

Use this orchestrator skill to guide a feature or bugfix from initial idea through specification, vertical-slice ticketization, parallel Test-Driven Development (TDD), and automated two-axis code review.

## Configuration

If `.agents/workflows/agentic-tdd-sdlc.yaml` exists in the workspace, read it first to honor project-specific settings:
- **Tracker mode:** `local` (default), `github`, `gitlab`, or `linear`
- **Local paths:** `docs/specs/` for specifications and `docs/tickets/` for ticket graphs
- **Concurrency:** `subagents.max_parallel` (default: `3`) and `subagents.workspace_mode` (default: `share`)

## End-to-End Lifecycle Phases

### Phase 1: Requirement Refinement (`/grill-me`)

- **Goal:** Stress-test the idea, uncover edge cases, resolve ambiguities, and align on architecture boundaries before writing specs or code.
- **How to run:**
  - Recommend the built-in `/grill-me` slash command to the user (`You can use the /grill-me command to interactively stress-test the requirements...`), or conduct a focused discovery interview until requirements and domain boundaries are clear.

### Phase 2: Specification Synthesis (`to-spec`)

- **Goal:** Synthesize the refined discussion and codebase context into a structured specification without re-interviewing the user.
- **Skill:** Read and follow [to-spec](../to-spec/SKILL.md).
- **Output:**
  - Local mode (default): `docs/specs/<feature-slug>.md`
  - External tracker mode: Published issue with the `ready-for-agent` label.

### Phase 3: Vertical-Slice Ticketization (`to-tickets`)

- **Goal:** Decompose the approved spec into independent tracer-bullet vertical slices with explicit `Blocked by` edges forming a directed acyclic task graph (DAG).
- **Skill:** Read and follow [to-tickets](../to-tickets/SKILL.md).
- **Output:**
  - Local mode (default): One markdown file per ticket in `docs/tickets/<feature-slug>/<NN>-<ticket-slug>.md` (ordered by dependency frontier).
  - External tracker mode: Linked sub-issues with native blocking relationships.

### Phase 4: Parallel TDD Implementation (`implement-spec` + `tdd`)

- **Goal:** Execute the ticket DAG along its unblocked frontier on an integration branch, enforcing a strict **Red → Green → Refactor** loop for every ticket.
- **Skills:** Read and follow [implement-spec](../implement-spec/SKILL.md), which delegates each ticket to an implementer subagent following [tdd](../tdd/SKILL.md).
- **Execution in `agy`:**
  - Spawn parallel implementer subagents via `invoke_subagent` (`TypeName: "self"`, `Workspace: "share"`) or orchestrate the frontier via `run_workflow` (`parallel()`).
  - Merge completed tickets into the integration branch, advance the frontier of newly unblocked tickets, and update ticket statuses to `done`.

### Phase 5: Two-Axis Code Review (`code-review`)

- **Goal:** Verify the completed integration branch against both **Standards** (documented repo conventions + Fowler code-smell baseline) and **Spec** (completeness, correctness, and zero scope creep).
- **Skill:** Read and follow [code-review](../code-review/SKILL.md).
- **Execution in `agy`:**
  - Spawn two read-only subagents (`TypeName: "research"`) in parallel—one for **Standards**, one for **Spec**—and aggregate their reports side by side.
  - If issues are raised, resolve them via a follow-up TDD cycle before finalizing the branch or PR.
