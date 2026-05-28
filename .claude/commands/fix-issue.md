---
description: Full automated pipeline — branch, analyse, develop, PR — for a GitHub issue
argument-hint: "[issue-number]"
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
---

Orchestrate the complete fix pipeline for issue $ARGUMENTS.

Execute each step in order. Do not skip any step. Do not stop until a pull request exists.

## Step 1 — Create branch
Follow the instructions in `.claude/commands/create-branch.md` using issue number $ARGUMENTS.

## Step 2 — Analyse the issue
Follow the instructions in `.claude/commands/analyze-issue.md` using issue number $ARGUMENTS.

## Step 3 — Implement the fix
Follow the instructions in `.claude/commands/develop.md`.
Apply every change identified in Step 2.

## Step 4 — Create pull request
Follow the instructions in `.claude/commands/create-pr.md` using issue number $ARGUMENTS.

A pull request MUST be created before this skill is considered complete.
If any step fails, report the error as a comment on the issue and stop.
