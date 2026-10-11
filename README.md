# Antigravity CLI (agy) TDD Multi-Agent Orchestrator Template

This repository serves as a centralized template for orchestrating multi-agent, test-driven development (TDD) workflows using the Antigravity CLI (`agy`) combined with modular engineering skills inspired by [Matt Pocock's skills repository](https://github.com/mattpocock/skills). It provides a standardized framework to transition from high-level feature requirements to structured specs, ticket graphs, parallel TDD execution, and automated code reviews.

## 🚀 Quick Bootstrap (One-Liner)

Instead of cloning or manually copying files, you can instantly bootstrap this workflow into any new or existing project repository by running:

```bash
curl -sSL https://raw.githubusercontent.com/mauicoder/agentic-workflow/main/setup.sh | bash
```

This will automatically fetch and configure the required `.agy/` configuration and static skill folders directly in your project workspace—**no Node.js or npm required**.

## Repository Structure

```text
.
├── .agy/
│   └── workflow.yaml          # Orchestration configuration & TDD guidelines
├── skills/
│   ├── agy-tdd-orchestrator/  # Core orchestration wrapper
│   ├── to-spec/               # Skill: Synthesize specs from discussions
│   ├── to-ticket/             # Skill: Break specs down into dependent tickets
│   └── implement-spec/        # Skill: Parallel TDD execution (Red-Green-Refactor)
├── setup.sh                   # Remote bootstrap script
└── README.md                  # Setup and usage guide
```

## 📋 The Complete End-to-End Workflow

Open your terminal in the root of your project workspace and launch `agy`, then execute the following command pipeline:

```bash
$ agy

# 1. Refine requirements interactively
/grill-me [your sketched idea, feature description, or bug report]

# 2. Transform the discussion into a formal specification
/to-spec

# 3. Slice the spec into structured, dependent tracer-bullet tickets
/to-ticket

# 4. Clear context to give subagents a fresh, clean execution state
/clear

# 5. Execute parallel TDD implementation (Red-Green-Refactor cycle)
/implement-spec

# 6. Run automated code review and feedback loops
/code-review
```

### Key Lifecycle Phases

1. **Requirements & Specs (`/grill-me` & `/to-spec`):** Fleshes out edge cases, acceptance criteria, and domain boundaries without polluting your active context.
2. **Ticket Slicing (`/to-ticket`):** Automatically maps out dependency trees and blocking edges so subagents know what contracts must be built first.
3. **TDD Implementation (`/implement-spec`):** Enforces a strict **Red-Green-Refactor** lifecycle:
   - **Red:** Subagents write failing unit/integration tests against interface contracts.
   - **Green:** Minimum production code is written to make tests pass.
   - **Refactor:** Code is cleaned up, duplication removed, and tests verified green.
4. **Code Review (`/code-review`):** Evaluates implementation diffs against the original specification to catch smells, edge cases, or contract drift.

## 🙏 Acknowledgments & Credits

Special thanks to **Matt Pocock** for his pioneering work on modular, model-invoked engineering skills (`mattpocock/skills`). This workflow adapts those concepts into a lightweight, shell-native structure compatible with `agy`.

## Customization

You can modify `.agy/workflow.yaml` per project to adjust execution parameters, max parallel subagents, or specific stack requirements (Python, Java/Kotlin, Kubernetes deployments, etc.).

## 🛠️ Troubleshooting

### 1. `Permission Denied` when running `./setup.sh` locally
If you downloaded the script locally using `curl -O` and try to execute it directly, you may encounter a permission error. Fix this by explicitly running it with `bash` or granting execution permissions:
```bash
# Option A: Run directly with bash
bash setup.sh

# Option B: Make it executable and run normally
chmod +x setup.sh
./setup.sh

