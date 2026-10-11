#!/usr/bin/env bash
set -e

REPO_RAW_URL="https://raw.githubusercontent.com/mauicoder/agentic-workflow/main"

echo "🚀 Fetching agy agentic workflow and skill packages..."

# 1. Create required local directories
mkdir -p .agy skills/agy-tdd-orchestrator skills/to-tickets skills/implement-spec docs

# 2. Download configuration and core skills
curl -sSL "$REPO_RAW_URL/.agy/workflow.yaml" -o .agy/workflow.yaml
curl -sSL "$REPO_RAW_URL/skills/agy-tdd-orchestrator/SKILL.md" -o skills/agy-tdd-orchestrator/SKILL.md
curl -sSL "$REPO_RAW_URL/skills/to-tickets/SKILL.md" -o skills/to-tickets/SKILL.md
curl -sSL "$REPO_RAW_URL/skills/implement-spec/SKILL.md" -o skills/implement-spec/SKILL.md

echo "✨ Setup complete! All orchestration configs and skills are ready."

