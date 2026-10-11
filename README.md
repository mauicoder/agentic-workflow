# Antigravity CLI (agy) TDD Multi-Agent Orchestrator Template

This repository serves as a centralized template for orchestrating multi-agent, test-driven development (TDD) workflows using the Antigravity CLI (`agy`). It provides a standardized framework to transition from high-level feature requirements to structured PRDs, dependency task graphs, and isolated, contract-first subagent executions.

## 🚀 Quick Bootstrap (One-Liner)

Instead of cloning or manually copying files, you can instantly bootstrap this workflow into any new or existing project repository by running:

```bash
curl -sSL https://raw.githubusercontent.com/mauicoder/agentic-workflow/main/setup.sh | bash
```

This will automatically fetch and configure the required `.agy/workflow.yaml` and agent skills directly in your project workspace.

---

## Repository Structure

```text
.
├── .agy/
│   └── workflow.yaml          # Default orchestration configuration & TDD rules
├── skills/
│   └── agy-tdd-orchestrator/
│       └── SKILL.md           # Reusable agent skill definition
├── setup.sh                   # Remote bootstrap script
└── README.md                  # Setup and usage guide
```

## How to Use the Workflow

### 1. Step 1: Requirements Gathering (`/grill-me`)

Open your terminal in the root of your project workspace and launch `agy`:

```bash
agy
```

Run the interactive refinement command with your high-level feature idea, bug, or system goal:

```bash
/grill-me [your sketched idea, feature description, or bug report]
```

The orchestrator will prompt you to flesh out edge cases, constraints, and acceptance criteria.

### 2. Step 2: Artifact Synthesis (PRD & Tasks)

Once the requirements session is complete, instruct the orchestrator to synthesize everything into documentation and a task dependency graph:

```bash
/goal "Synthesize our discussion into docs/PRD.md and generate tasks.json with explicit dependency mappings and interface contracts first."
```

### 3. Step 3: TDD Subagent Execution

Pass the generated task graph back into `agy` to dispatch specialized subagents following a strict Red-Green-Refactor TDD cycle and contract-first boundaries:

```bash
/goal "Execute tasks.json respecting dependencies. Ensure subagents write failing tests against interface contracts before implementing code."
```

## Customization

You can modify `.agy/workflow.yaml` per project to adjust execution parameters, max parallel subagents, or specific stack requirements (e.g., Python, Java/Kotlin, or Kubernetes configurations).