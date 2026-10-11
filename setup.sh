#!/usr/bin/env bash
set -e

REPO_RAW_URL="https://raw.githubusercontent.com/mauicoder/agentic-workflow/main"

echo "🚀 Fetching agy agentic workflow files from mauicoder/agentic-workflow..."

# 1. Create required local directories
mkdir -p .agy skills/agy-tdd-orchestrator docs

# 2. Download workflow configuration
echo "Downloading .agy/workflow.yaml..."
curl -sSL "$REPO_RAW_URL/.agy/workflow.yaml" -o .agy/workflow.yaml

# 3. Download the agent skill
echo "Downloading SKILL.md..."
curl -sSL "$REPO_RAW_URL/skills/agy-tdd-orchestrator/SKILL.md" -o skills/agy-tdd-orchestrator/SKILL.md

echo "✨ Setup complete! Your project is now ready for agy orchestration."

