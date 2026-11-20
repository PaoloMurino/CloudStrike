---
name: github-standardized-push
description: >-
  Fast, standardized Git commit and push to GitHub for multi-PC collaboration.
  Enforces Conventional Commits formatting and quick rebase-before-push sync.
  Use when the user asks to push, "fai il push", "pusha su github", "push
  standardizzato", or "committa e pusha".
metadata:
  category: workflow
  repo: CloudStrike
  version: "1.1"
---

# GitHub Standardized Push

Fast commit-and-push workflow with standardized commit formatting for multi-PC collaboration.

## Rules
- Never use `--force`, `-f`, or `--hard`.
- Never commit `.env` or `.DS_Store`.
- Always use non-interactive flags (`--no-pager`, `-m`).

## Commit Format (Conventional Commits)
Write commit messages in **English** using:

```text
<type>(<scope>): <short imperative summary>
```

- **Types:** `feat` | `fix` | `docs` | `refactor` | `chore`
- **Scopes:** `specs` | `steering` | `skills` | `hooks` | `docs` | `repo`
- **Style:** lowercase, imperative mood, max 72 chars, no trailing period.

**Examples:**
- `feat(specs): add requirements and acceptance criteria`
- `feat(steering): define architecture and coding constraints`
- `feat(hooks): add spec-alignment check on save`
- `docs(repo): update pitch overview in README`

## Fast Workflow

1. **Stage & inspect**
   ```bash
   git --no-pager status --short
   git add -A
   ```
   *(If nothing to commit and nothing ahead of remote, stop and report.)*

2. **Commit with standardized message**
   ```bash
   git commit -m "<type>(<scope>): <short imperative summary>"
   ```

3. **Sync (multi-PC) & push**
   ```bash
   BRANCH=$(git branch --show-current)
   git pull --rebase origin "$BRANCH"
   git push -u origin "$BRANCH"
   ```
   *(If rebase conflicts occur, run `git rebase --abort` and report the conflicting files.)*

4. **Confirm**
   Report one line: `<branch> | <short-sha> | <commit message>`.
