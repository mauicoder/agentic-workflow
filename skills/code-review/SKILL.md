---
name: code-review
description: >-
  Review changes between HEAD and a base ref (commit, branch, tag, or merge-base)
  along two independent axes in parallel subagents: Standards (repo coding standards
  + Fowler code smells) and Spec (compliance with the originating specification).
  Use when the user asks for a code review, runs /code-review, or after implement-spec completes.
---

# Two-Axis Code Review

Perform a two-axis review of the diff between `HEAD` and a fixed base point (`main`, a commit SHA, tag, or branch):

- **Standards Axis:** Does the code conform to the repository's documented coding standards and baseline refactoring heuristics?
- **Spec Axis:** Does the code faithfully and completely implement the originating specification without scope creep?

Both axes run as **parallel read-only subagents** so their contexts remain isolated, and this skill aggregates their findings side by side.

## Process

### 1. Pin the Fixed Point

1. Use the base ref provided by the user (e.g., `main`, `origin/main`, a commit SHA, tag, or `HEAD~N`). If none was specified and you are on a feature/integration branch, default to the repository's default branch (`main` or `master`); if still ambiguous, ask the user.
2. Verify the ref resolves (`git rev-parse --verify <fixed-point>`) and check the commit log (`git log <fixed-point>..HEAD --oneline`) and diff (`git diff <fixed-point>...HEAD --stat`).
3. If the diff is empty, stop and report that there are no changes between `<fixed-point>` and `HEAD`.

### 2. Identify the Spec Source

Locate the originating specification in this order:
1. A spec path or issue identifier explicitly passed by the user.
2. A spec file under `docs/specs/`, `specs/`, or `.scratch/` matching the branch name or referenced in `docs/tickets/`.
3. Issue references in commit messages (`#123`, `Closes #45`, etc.).
4. If no spec is found, ask the user where the spec is located. If the user confirms there is no spec, skip the **Spec** subagent and note `"No spec provided"` in the final report.

### 3. Identify the Standards Sources

Search the repository for files that document coding conventions or architecture rules, including:
- `AGENTS.md`, `GEMINI.md`, `.agents/rules/*.md`
- `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `README.md`, or `docs/adr/`

In addition to documented repo rules, the **Standards** axis always evaluates the **Fowler Code Smell Baseline** (_Refactoring_, ch. 3) below. Two rules govern it:
- **Repo standards override the baseline:** Where a documented repo convention endorses a pattern the baseline would flag, follow the repo convention.
- **Smells are judgement calls:** Documented-standard breaches can be hard violations, whereas baseline smells are heuristics. Skip formatting or lint rules already enforced by automated tooling.

#### Baseline Smells (*what it is* → *how to fix*)

- **Mysterious Name:** A function, variable, or type whose name doesn't reveal what it does or holds → rename it clearly.
- **Duplicated Code:** The same logic structure appears in multiple places in the diff → extract and reuse a shared abstraction.
- **Feature Envy:** A function/method reaches into another object's internal data more than its own → move behavior closer to the data.
- **Data Clumps:** The same group of parameters or fields repeatedly travel together → bundle them into a dedicated domain type.
- **Primitive Obsession:** Raw primitives/strings stand in for a domain concept with invariants → introduce a value object or domain type.
- **Repeated Switches:** The same `switch`/`if`-else chain over a type code recurs in multiple places → unify with polymorphism or a shared dispatch map.
- **Shotgun Surgery:** One logical change requires scattered edits across many unrelated files → consolidate cohesive responsibilities into one module.
- **Divergent Change:** One file or module is modified for several unrelated reasons → split so each module changes for a single reason.
- **Speculative Generality:** Unused hooks, parameters, or abstractions added for hypothetical future needs → remove them until required by a spec.
- **Message Chains:** Deep `a.b().c().d()` traversal coupling the caller to navigation structure → expose a direct intention-revealing method.
- **Middle Man:** A class or wrapper that only delegates without adding domain value → inline or call the target directly.
- **Refused Bequest:** A subclass or implementation that ignores or stubs out most of its interface contract → replace inheritance with composition or narrow the interface.

### 4. Spawn Both Review Subagents in Parallel

Launch two read-only subagents in parallel with `model="Gemini 4 Argon"` using `invoke_subagent` (`TypeName: "research"`, `Model: "Gemini 4 Argon"`) or `run_workflow` with `parallel()`:

```python
REVIEW_MODEL = "Gemini 4 Argon"

def create_review_agent(axis, prompt, model=REVIEW_MODEL):
    return agent(
        prompt=prompt,
        schema={"type": "string"},
        role=f"Code Review - {axis} Axis",
        type_name="research",
        workspace="inherit",
        model=model,
    )

reports = await parallel(
    [
        ("Standards", standards_prompt),
        ("Spec", spec_prompt),
    ],
    lambda item: create_review_agent(item[0], item[1], model=REVIEW_MODEL),
)
```

1. **Standards Reviewer (`Role: "Code Review - Standards Axis"`, `Model: "Gemini 4 Argon"`):**
   - Provide:
     - The exact diff command (`git diff <fixed-point>...HEAD`) and commit list.
     - Paths to all repo standards files discovered in Step 3, plus the **Baseline Smells** list above pasted in full.
   - Task instructions:
     > "Inspect `git diff <fixed-point>...HEAD`. Report per file/hunk: (a) any violation of a documented repo standard (cite the file and rule); and (b) any baseline code smell observed (name the smell and quote the relevant lines). Clearly label hard violations vs. judgement calls. Skip anything enforced by linters/formatters. Keep the report under 400 words."

2. **Spec Reviewer (`Role: "Code Review - Spec Axis"`, `Model: "Gemini 4 Argon"`):**
   - Provide:
     - The exact diff command (`git diff <fixed-point>...HEAD`) and commit list.
     - Path to (or contents of) the specification from Step 2 (and any associated tickets under `docs/tickets/`).
   - Task instructions:
     > "Compare `git diff <fixed-point>...HEAD` against the specification. Report: (a) requirements or acceptance criteria that are missing or only partially implemented; (b) unrequested behavior or scope creep introduced in the diff; and (c) requirements where the implementation contradicts the spec or misses an edge case. Quote the relevant spec requirement for each finding. Confirm whether tests cover the specified seams. Keep the report under 400 words."

### 5. Aggregate Side by Side

Present the two subagent reports under separate `## Standards` and `## Spec` headings without merging or re-ranking them across axes:
- Code that follows every coding convention but implements the wrong behavior is **Standards Pass / Spec Fail**.
- Code that satisfies every user story but violates architecture rules is **Spec Pass / Standards Fail**.

Conclude with a concise summary line showing the finding count per axis and the highest-priority action item within each axis.
