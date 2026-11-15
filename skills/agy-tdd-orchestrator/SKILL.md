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
- **Multi-Model Phase Allocation:**
  - **Architecture, Spec-Generation, and Final Orchestrator/Merge Phases:** `"Gemini 4 Argon"` (`models.architecture`, `models.specification`, `models.ticketization`, `models.orchestrator`, `models.merge`, `models.review`)
  - **Parallel Ticket Implementation & Coding Agents:** `"Gemini 4 Hydrogen"` (`models.implementation` / `subagents.models.coding`)
- **Python Workflow Script:** `.agents/workflows/agentic-tdd-sdlc.py` (can be executed via `run_workflow` with `ScriptPath`)

## End-to-End Lifecycle Phases

### Phase 1: Requirement Refinement & Architecture (`/grill-me`)

- **Model:** `"Gemini 4 Argon"`
- **Goal:** Stress-test the idea, uncover edge cases, resolve ambiguities, and align on architecture boundaries before writing specs or code.
- **How to run:**
  - Recommend the built-in `/grill-me` slash command to the user (`You can use the /grill-me command to interactively stress-test the requirements...`), or conduct a focused discovery interview using `"Gemini 4 Argon"` until requirements and domain boundaries are clear.

### Phase 2: Specification Synthesis (`to-spec`)

- **Model:** `"Gemini 4 Argon"`
- **Goal:** Synthesize the refined discussion and codebase context into a structured specification without re-interviewing the user.
- **Skill:** Read and follow [to-spec](../to-spec/SKILL.md) (passing `model="Gemini 4 Argon"` when instantiated via workflow/subagent).
- **Output:**
  - Local mode (default): `docs/specs/<feature-slug>.md`
  - External tracker mode: Published issue with the `ready-for-agent` label.

### Phase 3: Vertical-Slice Ticketization (`to-tickets`)

- **Model:** `"Gemini 4 Argon"`
- **Goal:** Decompose the approved spec into independent tracer-bullet vertical slices with explicit `Blocked by` edges forming a directed acyclic task graph (DAG).
- **Skill:** Read and follow [to-tickets](../to-tickets/SKILL.md) (passing `model="Gemini 4 Argon"` when instantiated via workflow/subagent).
- **Output:**
  - Local mode (default): One markdown file per ticket in `docs/tickets/<feature-slug>/<NN>-<ticket-slug>.md` (ordered by dependency frontier).
  - External tracker mode: Linked sub-issues with native blocking relationships.

### Phase 4: Parallel TDD Implementation (`implement-spec` + `tdd`)

- **Coding Agent Model:** `"Gemini 4 Hydrogen"`
- **Orchestrator / Merge Model:** `"Gemini 4 Argon"`
- **Goal:** Execute the ticket DAG along its unblocked frontier on an integration branch, enforcing a strict **Red → Green → Refactor** loop for every ticket.
- **Skills:** Read and follow [implement-spec](../implement-spec/SKILL.md), which delegates each ticket to an implementer subagent following [tdd](../tdd/SKILL.md).
- **Execution in `agy`:**
  - Spawn parallel implementer coding agents with `model="Gemini 4 Hydrogen"` (`workspace="share"`), or execute `.agents/workflows/agentic-tdd-sdlc.py` via `run_workflow`.
  - Use `"Gemini 4 Argon"` for the orchestrator/merge step to integrate completed ticket branches into `feat/<feature-slug>`, run the integration test suite, advance the frontier of newly unblocked tickets, and update ticket statuses to `done`.

### Phase 5: Final Orchestrator Merge & Two-Axis Code Review (`code-review`)

- **Model:** `"Gemini 4 Argon"`
- **Goal:** Finalize the integration branch merge and verify it against both **Standards** (documented repo conventions + Fowler code-smell baseline) and **Spec** (completeness, correctness, and zero scope creep).
- **Skill:** Read and follow [code-review](../code-review/SKILL.md).
- **Execution in `agy`:**
  - Spawn two read-only review agents (`type_name="research"`, `model="Gemini 4 Argon"`) in parallel—one for **Standards**, one for **Spec**—and aggregate their reports side by side in the final `"Gemini 4 Argon"` orchestrator phase.
  - If issues are raised, resolve them via a follow-up `"Gemini 4 Hydrogen"` TDD coding agent and re-verify on the integration branch with `"Gemini 4 Argon"`.

## Python Workflow Definition (`run_workflow`)

When orchestrating phases programmatically via `run_workflow`, run `.agents/workflows/agentic-tdd-sdlc.py` or pass the `model` parameter explicitly to every `agent(...)` instantiation:

```python
ARCHITECT_MODEL = "Gemini 4 Argon"
CODING_MODEL = "Gemini 4 Hydrogen"

def spawn_phase_agent(prompt, schema, role, model, type_name="self", workspace="inherit"):
    return agent(
        prompt=prompt,
        schema=schema,
        role=role,
        type_name=type_name,
        workspace=workspace,
        model=model,
    )

phase("Architecture & Spec Generation")
spec_info = await spawn_phase_agent(
    prompt="Synthesize architecture into docs/specs/<slug>.md and slice tickets under docs/tickets/<slug>/.",
    schema={"type": "object", "properties": {"spec": {"type": "string"}, "tickets": {"type": "array", "items": {"type": "string"}}}, "required": ["spec", "tickets"]},
    role="Architecture & Spec Generator",
    model=ARCHITECT_MODEL,
)

phase("Parallel Ticket Implementation")
ticket_results = await parallel(
    spec_info["tickets"],
    lambda t: spawn_phase_agent(
        prompt=f"Implement {t} following skills/tdd/SKILL.md (Red -> Green -> Refactor).",
        schema={"type": "string"},
        role=f"TDD Coding Agent ({t})",
        workspace="share",
        model=CODING_MODEL,
    ),
)

phase("Final Orchestrator & Merge")
merge_summary = await spawn_phase_agent(
    prompt=f"Merge completed ticket branches ({ticket_results}), run full test suite, and complete two-axis code review.",
    schema={"type": "string"},
    role="Final Orchestrator & Merge",
    model=ARCHITECT_MODEL,
)
```
