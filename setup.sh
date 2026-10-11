#!/usr/bin/env bash
set -e

REPO_RAW_URL="https://raw.githubusercontent.com/mauicoder/agentic-workflow/main"

echo "🚀 Initializing agy agentic workflow..."

# 1. Create required directories
mkdir -p .agy skills/agy-tdd-orchestrator skills/to-spec skills/to-ticket skills/implement-spec docs/specs

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

# 3. Pull configurations and skills
download_file "$REPO_RAW_URL/.agy/workflow.yaml" ".agy/workflow.yaml"
download_file "$REPO_RAW_URL/skills/agy-tdd-orchestrator/SKILL.md" "skills/agy-tdd-orchestrator/SKILL.md"
download_file "$REPO_RAW_URL/skills/to-spec/SKILL.md" "skills/to-spec/SKILL.md"
download_file "$REPO_RAW_URL/skills/to-ticket/SKILL.md" "skills/to-ticket/SKILL.md"
download_file "$REPO_RAW_URL/skills/implement-spec/SKILL.md" "skills/implement-spec/SKILL.md"

echo "✨ Setup complete! All orchestration configs and skills are ready."

