---
description: Create a git branch for a GitHub issue
argument-hint: "[issue-number]"
allowed-tools: Bash
---

Create a new git branch scoped to the issue number provided in $ARGUMENTS.

Steps:
1. Make sure the working tree is clean: `git status`
2. Switch to main and pull latest: `git checkout main && git pull origin main`
3. Create and switch to the new branch: `git checkout -b fix/issue-$ARGUMENTS`
4. Confirm with: `git branch --show-current`
