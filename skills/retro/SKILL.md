---
name: retro
description: >-
  Conduct a post-session or post-workflow retrospective in Antigravity (agy) to
  identify environment, guardrail, standard, and multi-agent workflow improvements
  based on current interactions, implementation history, subagent feedback, code
  review findings, and session transcripts. Use when the user asks for a retro,
  runs /retro, or as Phase 6 after code-review completes.
---

# Retrospective & Continuous Improvement (`retro`)

Conduct a structured **retrospective** on a coding session or multi-agent TDD workflow run to improve future runs. Analyze concrete friction, defects, and token waste across the session, save a severity-ranked retrospective report to `docs/retros/<feature-slug>.md`, and discuss proposed changes with the user before modifying steering files, skills, or checks.

## Steps

### 1. Load Agent-Writing Guidelines

Read [`.agents/skills/writing-for-agents/SKILL.md`](../writing-for-agents/SKILL.md) (or `skills/writing-for-agents/SKILL.md`) and [`SKILL-MECHANICS.md`](../writing-for-agents/SKILL-MECHANICS.md) before drafting any recommendations for steering files, rules, or skills.

### 2. Gather Primary Sources

Inspect the primary evidence from the specified session or feature run (defaulting to the current session/feature if unspecified):

1. **Subagent Feedback & Friction:** Inspect structured `feedback` fields returned by TDD coding agents (`Gemini 4 Hydrogen`), wave merge orchestrators, and final orchestrator agents.
2. **Two-Axis Code Review Findings:** Inspect the Phase 5 `Standards` and `Spec` review reports for violations, code smells, missed requirements, or scope creep that slipped past implementation.
3. **Specs, Tickets & Git History:**
   - Read `docs/specs/<feature-slug>.md` and `docs/tickets/<feature-slug>/*.md` to check whether ticket boundaries or testing seams were ambiguous.
   - Check `git log` and commit diffs on `feat/<feature-slug>` for retry commits, merge conflicts between parallel waves, or post-review fixups.
4. **Antigravity Session & Subagent Transcripts:**
   - Inspect `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` (typically under `~/.gemini/antigravity-cli/brain/<conversation-id>/.system_generated/logs/transcript.jsonl`).
   - When `truncated_fields` is present on a relevant step, read the corresponding line in `transcript_full.jsonl`.
   - Grep for `invoke_subagent` or `run_workflow` in `transcript.jsonl` to locate child subagent conversation IDs and inspect their transcripts for tool errors, blind searches, or repeated test failures.

### 3. Evaluate Improvement Candidates by Category

Look for high-leverage improvement candidates across these categories:

- **Navigation**: How easy was it for agents to find the right files and seams? Were there hidden cross-file dependencies? Would a concise **context pointer** in `AGENTS.md`, `GEMINI.md`, or `.agents/rules/` eliminate blind search? _Use when_ an agent spent multiple turns searching for an entry point, test helper, or contract.
- **Automated checks**: Are there deterministic checks that could have caught errors an agent made (linting, typechecking, unit/integration tests, filesystem/import linters)? Read the repo's existing check commands first (`package.json`, `Makefile`, `pyproject.toml`, `build.gradle`, CI workflows) so an existing check that sits unwired or broken is the finding—not a reinvention. A repo with no **guardrail** (no pre-commit hook and no CI job running lint/typecheck/test) is itself a high-severity finding. _Use when_ an agent made a mistake an automated check could catch, or the repo lacks guardrails.
- **Coding standards**: Should the **Standards reviewer** be given a new rule to enforce, or should an existing rule be clarified or pruned? Classify the violation first:
  - A **mechanical** rule (fixed syntactic pattern, banned API, import boundary, file-location convention) gets a deterministic check (custom linter rule, pre-commit hook, or CI check), full stop. Default to building the check over writing prose.
  - Reserve `CODING_STANDARDS.md` for genuine **judgement calls** (cross-file design consistency, domain naming nuances, architectural trade-offs no static guardrail can verify). _Use when_ the reviewer agent missed an issue or flagged noise.
- **Global & Workspace Steering (`AGENTS.md`, `GEMINI.md`, `.agents/rules/`)**: Are there steering instructions sitting in always-loaded context that belong in `CODING_STANDARDS.md` (read only during review) or in automated checks? _Use when_ always-loaded steering files are bloated or carry review-only rules.
- **Multi-Agent Workflow & Skill Tuning**: Did friction originate in how the workflow orchestrated work? Check for:
  - **Spec & Ticket Slicing (`to-spec` / `to-tickets`):** Were tickets sliced horizontally instead of vertically, or were `Blocked by` dependencies missing—causing parallel `Gemini 4 Hydrogen` coding agents to collide on the same files during wave merges?
  - **TDD Loop (`tdd` / `implement-spec`):** Did coding agents struggle with test harness setup, mock boundaries, or workspace isolation (`share` vs `branch`)?
  - **Prompts & Schemas (`.agents/skills/*`, `.agents/workflows/*`):** Did a skill prompt leave a completion criterion vague, inviting premature completion? _Use when_ subagent feedback, merge conflicts, or review failures point to workflow/skill instructions.
- **Tool economy**: Did agents make expensive or repetitive tool calls (e.g., running full test suites instead of targeted tests, reading massive generated files, or invoking token-heavy CLI outputs)? _Use when_ transcripts show avoidable token or wall-clock waste.
- **No-ops & Sediment**: Look for instructions in steering files or skills that fail to modify agent behavior beyond default priors, or stale instructions that restate what the environment already tells the agent. _Use when_ steering files or skills accumulate dead weight.
- **Information access**: Was crucial runtime or environment information missing (e.g., silent test runner output, missing fixture documentation, unexposed dev server logs)? _Use when_ an agent had to guess because a signal was hidden.

### 4. Persist Report, Present Ranked Candidates, and Confirm Before Applying

1. **Save the Retrospective Report:** Write a structured markdown report to `docs/retros/<feature-slug>.md` (or `docs/retros/<YYYY-MM-DD>-<session-slug>.md` for standalone sessions) containing:
   - **Run Summary:** Feature/session scope, ticket waves executed, review outcomes, and key friction signals.
   - **Subagent Feedback Digest:** Consolidated issues reported by coding, merge, and review agents.
   - **Ranked Improvement Candidates:** Ordered by severity (`High` → `Medium` → `Low`), citing the category, concrete evidence (transcript step, commit, or subagent feedback), target file/check, and exact proposed change.
2. **Present & Discuss with the User:** Present the severity-ranked candidates concisely in chat and link to `docs/retros/<feature-slug>.md`.
3. **Confirm Before Mutating Environment:** Discuss and get explicit user confirmation before applying any edits to `AGENTS.md`, `GEMINI.md`, `.agents/rules/`, `CODING_STANDARDS.md`, `.agents/skills/`, `.agents/workflows/`, or repository linters/hooks.

## Reference

### Implementation vs. Review Context Pressure

All feature work flows through distinct cognitive stages with different context budgets:

- **Implementation Agents (`Gemini 4 Hydrogen`)** experience the highest **context pressure**: they explore seams, run the Red → Green → Refactor loop, and debug test failures. Keep their always-loaded context lean—push non-essential prose out of `AGENTS.md`/`GEMINI.md` and rely on deterministic test/lint feedback.
- **Review & Orchestrator Agents (`Gemini 4 Argon`)** experience lower exploration pressure during review because they inspect a bounded diff (`git diff <base>...HEAD`) against `CODING_STANDARDS.md` and `docs/specs/<feature-slug>.md`. Coding standards that require human-like judgement belong in `CODING_STANDARDS.md` (enforced during `code-review`), not in the implementer's always-loaded steering files.

### Target Files in an `agy` Workspace

- `AGENTS.md` / `GEMINI.md` / `.agents/rules/*.md`: Loaded into the context window of agents working in the repo. Use sparingly—primarily for high-signal **context pointers** and critical environment commands.
- `CODING_STANDARDS.md`: Read by the **Standards** reviewer during `code-review`, not during implementation. Add context pointers to `docs/` if standards grow beyond 1,000 lines.
- `docs/specs/`, `docs/tickets/`, `docs/retros/`: Local artifacts for specifications, dependency-graphed tickets, and retrospective reports.
- `.agents/skills/<skill>/SKILL.md` (template source: `skills/<skill>/SKILL.md`): Modular skills discovered via their frontmatter `description`. Follow [`writing-for-agents`](../writing-for-agents/SKILL.md) when refining skill steps, completion criteria, or context pointers.
- `.agents/workflows/` (template source: `workflows/`): Multi-model workflow orchestration scripts (`agentic-tdd-sdlc.py`, `agentic-tdd-sdlc.yaml`, `workflow.json`).
