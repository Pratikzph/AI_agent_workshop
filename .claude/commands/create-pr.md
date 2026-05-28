---
description: Commit all changes, push the branch, and open a pull request
argument-hint: "[issue-number]"
allowed-tools: Bash
---

Commit every staged change and open a pull request that closes the issue.

Steps:
1. Stage all changes: `git add -A`
2. Check what will be committed: `git diff --cached --stat`
3. Commit: `git commit -m "fix: resolve issue #$ARGUMENTS"`
4. Push: `git push origin HEAD`
5. Create the PR:
   ```
   gh pr create \
     --title "fix: <concise description derived from the changes>" \
     --body "$(printf '## Summary\nDescribe what was wrong and how it was fixed.\n\n## Changes\n- list each file changed and why\n\n## How to verify\nSteps to confirm the fix works.\n\nCloses #'$ARGUMENTS)" \
     --base main
   ```
6. Capture the PR URL from the output of the previous command.
7. Post a comment on the issue:
   `gh issue comment $ARGUMENTS --body "I have opened a pull request with a fix: <PR URL>"`
