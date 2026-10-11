#!/usr/bin/env bash
set -e

REPO_RAW_URL="https://raw.githubusercontent.com/mauicoder/agentic-workflow/main"

echo "🚀 Initializing agy agentic workflow..."

# Ensure we are inside a git repository root or warn the user
if [ ! -d ".git" ]; then
    echo "⚠️ Warning: Not a git repository root. Continuing anyway..."
fi

# 1. Create required local directories
mkdir -p .agy skills/agy-tdd-orchestrator skills/to-tickets skills/implement-spec docs

# 2. Helper function to safely download files
download_file() {
    local src="$1"
    local dest="$2"
    echo "Downloading $dest..."
    if ! curl -sSL --fail "$src" -o "$dest"; then
        echo "❌ Error: Failed to download $src" >&2
        exit 1
    fi
}

# 3. Fetch configs and skills
download_file "$REPO_RAW_URL/.agy/workflow.yaml" ".agy/workflow.yaml"
download_file "$REPO_RAW_URL/skills/agy-tdd-orchestrator/SKILL.md" "skills/agy-tdd-orchestrator/SKILL.md"
download_file "$REPO_RAW_URL/skills/to-tickets/SKILL.md" "skills/to-tickets/SKILL.md"
download_file "$REPO_RAW_URL/skills/implement-spec/SKILL.md" "skills/implement-spec/SKILL.md"

echo "✨ Setup complete! All orchestration configs and skills are ready."

