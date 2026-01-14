#!/bin/bash

# Script to pull all updates including submodules for Raspberry Pi
# Usage: ./pull.sh

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${CYAN}${BOLD}Starting update process...${NC}"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Get current branch (should be dev)
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}Current branch: ${BOLD}$CURRENT_BRANCH${NC}"

# Pull main repository
echo ""
echo -e "${CYAN}Pulling main repository (branch: $CURRENT_BRANCH)...${NC}"
if ! git pull origin "$CURRENT_BRANCH"; then
    echo -e "${RED}${BOLD}Failed to pull main repository${NC}"
    exit 1
fi
echo -e "${GREEN}Main repository updated${NC}"

# Initialize and update submodules
echo ""
echo -e "${CYAN}Initializing submodules...${NC}"
git submodule update --init --recursive

# Update each submodule to dev branch (or main if dev doesn't exist)
echo ""
echo -e "${CYAN}Updating submodules...${NC}"

# Function to update submodule
update_submodule() {
    local submodule_path=$1
    local submodule_name=$(basename "$submodule_path")
    local target_branch="dev"
    
    if [ ! -d "$submodule_path" ]; then
        echo -e "    ${YELLOW}Warning: $submodule_path not found${NC}"
        return
    fi
    
    echo -e "  ${MAGENTA}Updating $submodule_name...${NC}"
    cd "$submodule_path"
    
    # Fetch all branches
    git fetch origin 2>/dev/null || true
    
    # Check if dev branch exists on remote
    if git ls-remote --heads origin dev | grep -q dev; then
        target_branch="dev"
    elif git ls-remote --heads origin main | grep -q main; then
        target_branch="main"
    else
        # Try to get default branch
        target_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    fi
    
    # Checkout target branch
    if git show-ref --verify --quiet refs/heads/"$target_branch"; then
        git checkout "$target_branch"
    else
        git checkout -b "$target_branch" origin/"$target_branch" 2>/dev/null || {
            echo -e "    ${YELLOW}Warning: Failed to checkout $target_branch in $submodule_name${NC}"
            cd "$SCRIPT_DIR"
            return
        }
    fi
    
    # Pull latest changes
    if git pull origin "$target_branch"; then
        echo -e "    ${GREEN}$submodule_name updated (branch: $target_branch)${NC}"
    else
        echo -e "    ${YELLOW}Warning: Failed to pull $submodule_name${NC}"
    fi
    
    cd "$SCRIPT_DIR"
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
echo -e "${GREEN}${BOLD}Update completed successfully!${NC}"

