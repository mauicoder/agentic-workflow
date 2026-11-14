# Antigravity CLI (`agy`) TDD Multi-Agent Orchestrator Template

This repository serves as a centralized template for orchestrating multi-agent, test-driven development (TDD) workflows using the Antigravity CLI (`agy`) combined with modular engineering skills inspired by [Matt Pocock's skills repository](https://github.com/mattpocock/skills). It provides a standardized framework to transition from high-level feature requirements to structured specifications, dependency-graphed tickets, parallel TDD execution, and automated two-axis code reviews.

## 🚀 Quick Bootstrap (One-Liner)

Instead of cloning or manually copying files, you can bootstrap this workflow into any new or existing project repository by running:

```bash
curl -sSL https://raw.githubusercontent.com/mauicoder/agentic-workflow/main/setup.sh | bash
```

This automatically creates the `.agents/` workspace customization hierarchy (`.agents/skills/` and `.agents/workflows/`) along with local `docs/specs/` and `docs/tickets/` directories—**no Node.js or npm required**.

## Repository Structure

```text
.
├── workflows/
│   └── agentic-tdd-sdlc.yaml      # Orchestration configuration & TDD guidelines
├── skills/
│   ├── agy-tdd-orchestrator/      # Core end-to-end lifecycle orchestrator skill
│   │   └── SKILL.md
│   ├── to-spec/                   # Skill: Synthesize specs from discussions
│   │   └── SKILL.md
│   ├── to-tickets/                # Skill: Slice specs into a dependency graph of tickets
│   │   └── SKILL.md
│   ├── implement-spec/            # Skill: Parallel frontier execution across subagents
│   │   └── SKILL.md
│   ├── tdd/                       # Skill: Strict Red-Green-Refactor loop per ticket
│   │   └── SKILL.md
│   └── code-review/               # Skill: Parallel two-axis review (Standards + Spec)
│       └── SKILL.md
├── setup.sh                       # Remote bootstrap script (installs into .agents/)
└── README.md                      # Setup and usage guide
```

When `setup.sh` runs in a target project, it installs these files into `.agents/workflows/agentic-tdd-sdlc.yaml` and `.agents/skills/<skill-name>/SKILL.md`, where `agy` automatically discovers them via progressive disclosure.

## 📋 The Complete End-to-End Workflow

Open your terminal in the root of your project workspace and launch `agy`, then progress through the five phases:

```bash
$ agy

# 1. Refine requirements interactively (built-in agy slash command)
/grill-me [your sketched idea, feature description, or bug report]

# 2. Synthesize the discussion into a formal specification (docs/specs/<slug>.md)
Use the to-spec skill to write the specification for this feature.

# 3. Slice the spec into dependency-graphed tracer-bullet tickets (docs/tickets/<slug>/)
Use the to-tickets skill to break the spec into vertical-slice tickets.

# 4. Compact context if needed before kicking off implementation
/compact

# 5. Execute parallel TDD implementation along the ticket frontier
Use the implement-spec skill to implement the tickets with TDD subagents.

# 6. Run automated two-axis code review (Standards + Spec)
Use the code-review skill to review the changes against main.
```

### Key Lifecycle Phases

1. **Requirements & Specs (`/grill-me` & `to-spec`):** Uncovers edge cases, testing seams, acceptance criteria, and domain boundaries, saving the synthesized specification to `docs/specs/<feature-slug>.md`.
2. **Ticket Slicing (`to-tickets`):** Decomposes the spec into vertical tracer-bullet tickets under `docs/tickets/<feature-slug>/<NN>-<ticket-slug>.md` with explicit `Blocked by` edges so subagents know which interface contracts must be built first.
3. **Parallel TDD Implementation (`implement-spec` & `tdd`):** Executes unblocked frontier tickets concurrently in isolated `agy` subagent workspaces (`Workspace: "share"`), enforcing a strict **Red → Green → Refactor** loop:
   - **Red:** Write a failing behavioral test against the target seam or contract.
   - **Green:** Write the minimum production code required to make the test pass.
   - **Refactor:** Clean up duplication and code smells while keeping all tests green.
4. **Two-Axis Code Review (`code-review`):** Spawns two parallel read-only `research` subagents to evaluate the branch diff against:
   - **Standards:** Documented project conventions plus Fowler's refactoring code-smell baseline.
   - **Spec:** Completeness, behavioral accuracy, and zero scope creep relative to the originating spec.

## ⚙️ Customization

Edit `.agents/workflows/agentic-tdd-sdlc.yaml` (or [workflows/agentic-tdd-sdlc.yaml](file:///Users/maui/StudioProjects/agentic-workflow/workflows/agentic-tdd-sdlc.yaml) in this template) per project to adjust:
- `tracker.mode`: `"local"` (default markdown files in `docs/specs/` and `docs/tickets/`) or external issue trackers (`"github"`, `"gitlab"`, `"linear"`).
- `subagents.max_parallel`: Maximum concurrent TDD implementer subagents (default: `3`).
- `subagents.workspace_mode`: Subagent workspace isolation mode (`"share"` or `"branch"`).

## 🙏 Acknowledgments & Credits

Special thanks to **Matt Pocock** for his pioneering work on modular engineering skills (`mattpocock/skills`). This workflow adapts those concepts into a shell-native structure tailored for `agy`'s customization system and subagent primitives.

## 🛠️ Troubleshooting

### 1. `Permission Denied` when running `./setup.sh` locally
If you downloaded the script locally using `curl -O` and try to execute it directly, you may encounter a permission error. Fix this by explicitly running it with `bash` or granting execution permissions:

```bash
# Option A: Run directly with bash
bash setup.sh

# Option B: Make it executable and run normally
chmod +x setup.sh
./setup.sh
```
