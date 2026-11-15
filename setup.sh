#!/usr/bin/env bash
set -euo pipefail

REPO_RAW_URL="https://raw.githubusercontent.com/mauicoder/agentic-workflow/main"

echo "🚀 Initializing agy agentic TDD workflow..."

# 1. Create required directories
mkdir -p \
    .agents/workflows \
    .agents/skills/agy-tdd-orchestrator \
    .agents/skills/to-spec \
    .agents/skills/to-tickets \
    .agents/skills/implement-spec \
    .agents/skills/tdd \
    .agents/skills/code-review \
    docs/specs \
    docs/tickets

# 2. Safe download helper function
download_file() {
    local src="$1"
    local dest="$2"
    echo "Downloading $dest..."
    if ! curl -sSL --fail "$src" -o "$dest"; then
        echo "❌ Error: Failed to download $src" >&2
        exit 1
    fi
}

# 3. Pull workflow configuration, Python workflow definitions, and skills
download_file "$REPO_RAW_URL/workflows/agentic-tdd-sdlc.yaml" ".agents/workflows/agentic-tdd-sdlc.yaml"
download_file "$REPO_RAW_URL/workflows/agentic-tdd-sdlc.py" ".agents/workflows/agentic-tdd-sdlc.py"
download_file "$REPO_RAW_URL/workflows/workflow.json" ".agents/workflows/workflow.json"
download_file "$REPO_RAW_URL/skills/agy-tdd-orchestrator/SKILL.md" ".agents/skills/agy-tdd-orchestrator/SKILL.md"
download_file "$REPO_RAW_URL/skills/to-spec/SKILL.md" ".agents/skills/to-spec/SKILL.md"
download_file "$REPO_RAW_URL/skills/to-tickets/SKILL.md" ".agents/skills/to-tickets/SKILL.md"
download_file "$REPO_RAW_URL/skills/implement-spec/SKILL.md" ".agents/skills/implement-spec/SKILL.md"
download_file "$REPO_RAW_URL/skills/tdd/SKILL.md" ".agents/skills/tdd/SKILL.md"
download_file "$REPO_RAW_URL/skills/code-review/SKILL.md" ".agents/skills/code-review/SKILL.md"

echo "✨ Setup complete! All orchestration configs and skills are installed in .agents/"
