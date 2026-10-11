---
name: agy-tdd-orchestrator
description: Orchestrates a multi-agent TDD workflow using the Antigravity CLI (agy) through grill-me requirements, PRD generation, dependency mapping, and test-driven implementation. Use when setting up automated multi-agent coding sessions with agy.
---
# Antigravity TDD Multi-Agent Orchestrator

Use this workflow to transition from high-level feature ideas to fully orchestrated, TDD-compliant multi-agent executions using `agy`.

## Workflow Steps

1. **Requirement Gathering:**
   Run the interactive refinement tool to flesh out edge cases and acceptance criteria:
   ```bash
   agy
   /grill-me [feature description]

