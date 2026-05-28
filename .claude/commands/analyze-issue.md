---
description: Read a GitHub issue and summarise what needs to be built or fixed
argument-hint: "[issue-number]"
allowed-tools: Bash, Read, Glob, Grep
---

Analyse the GitHub issue and produce a clear implementation plan.

Steps:
1. Fetch the issue: `gh issue view $ARGUMENTS --json title,body,labels`
2. Read the full issue title and body carefully.
3. Use Glob and Grep to map the relevant parts of the codebase.
4. Produce a short plan:
   - What is broken or missing?
   - Which files need to change or be created?
   - What is the minimal change that resolves the issue?
5. Output the plan as a numbered list before proceeding.
