#!/bin/bash

# Script to pull all updates including submodules for Raspberry Pi
# Usage: ./pull.sh

set -e  # Exit on error

echo "🔄 Starting update process..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Get current branch (should be dev)
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Current branch: $CURRENT_BRANCH"

# Pull main repository
echo ""
echo "📥 Pulling main repository (branch: $CURRENT_BRANCH)..."
git pull origin "$CURRENT_BRANCH" || {
    echo "❌ Failed to pull main repository"
    exit 1
}

# Initialize and update submodules
echo ""
echo "📦 Updating submodules..."
git submodule update --init --recursive

# Update each submodule to dev branch
echo ""
echo "🔄 Updating submodules to dev branch..."

# Function to update submodule
update_submodule() {
    local submodule_path=$1
    local submodule_name=$(basename "$submodule_path")
    
    if [ -d "$submodule_path" ]; then
        echo "  → Updating $submodule_name..."
        cd "$submodule_path"
        
        # Checkout dev branch (create if doesn't exist)
        git fetch origin dev 2>/dev/null || true
        if git show-ref --verify --quiet refs/heads/dev; then
            git checkout dev
        else
            git checkout -b dev origin/dev 2>/dev/null || git checkout dev
        fi
        
        # Pull latest changes
        git pull origin dev || {
            echo "    ⚠️  Warning: Failed to pull $submodule_name"
        }
        
        cd "$SCRIPT_DIR"
        echo "    ✅ $submodule_name updated"
    else
        echo "    ⚠️  Warning: $submodule_path not found"
    fi
}

# Update each submodule
if [ -f .gitmodules ]; then
    while IFS= read -r line; do
        if [[ $line =~ ^[[:space:]]*path[[:space:]]*=[[:space:]]*(.+)$ ]]; then
            submodule_path="${BASH_REMATCH[1]}"
            update_submodule "$submodule_path"
        fi
    done < .gitmodules
fi

echo ""
echo "✅ Update completed successfully!"
echo ""
echo "📋 Summary:"
echo "  - Main repository: updated to latest $CURRENT_BRANCH"
echo "  - Submodules: updated to latest dev branch"
echo ""
echo "💡 Next steps:"
echo "  - Apply database migrations: docker compose -f docker-compose-amd64.yml exec api alembic upgrade head"
echo "  - Restart services if needed: docker compose -f docker-compose-amd64.yml restart"

