---
name: work-issue
description: Work a GitHub issue end-to-end — read the thread, gate on scope, branch, implement with conventional commits, open a PR that closes the issue, and squash-merge after explicit confirmation. Use when asked to work, fix, or implement a GitHub issue by number.
---

Work the given GitHub issue of this repository end-to-end. Use the base
branch the user names; if none, default to `main`.

## 1. Fetch & assess

- Read the full thread, not just the body — decisions often live in the
  comments: `gh issue view <number> --comments`.
- If the issue embeds images or attachments
  (`https://github.com/user-attachments/...`), fetch them with
  `curl -sL -H "Authorization: token $(gh auth token)" -o <tmpfile> <url>`
  and read them.
- **Scope gate — assess before touching anything:**
  - **Too big** (multi-session epic, several independent deliverables, or
    acceptance criteria too vague to verify): say so, recommend splitting the
    issue or decomposing the work first (e.g. a staged-rollout plan, if that
    plugin is installed), and **stop**.
  - **Too small** (a trivial one-liner where branch/PR ceremony is pure
    overhead): say so and offer to just make the change directly on the
    current branch instead. **Stop and wait** for the choice.
  - Otherwise: state a 1–3 line plan and continue without asking.

## 2. Branch

- `git fetch origin`, then branch off the base:
  `git switch -c <type>/<number>-<slug> origin/<base>`.
- `<type>`: the conventional-commit type matching the issue — `feat`, `fix`,
  `docs`, `refactor`, `test`, or `chore`.
- `<slug>`: 2–5 kebab-case words distilled from the issue title.
- Example: `fix/42-hook-crash-on-empty-plan`.

## 3. Implement & commit

- Do the work following the repo's conventions (CLAUDE.md, existing style,
  existing dependencies).
- Commit each logical unit as you go with conventional commit messages —
  don't batch everything into one commit at the end.
- If the repo keeps a changelog, add the entry as part of the work.

## 4. Pull request

- Push the branch and open the PR against the base:
  `gh pr create --base <base>`.
- PR description: what changed and why, any decisions or trade-offs worth a
  reviewer's attention, and `Closes #<number>` so the merge auto-closes the
  issue.

## 5. Merge — confirmation required

- Present the PR link and ask for explicit confirmation to merge. **Never
  merge without it.** If confirmation doesn't come, leave the PR open and
  finish the session cleanly.
- On OK: **squash merge** (unless the repo's own conventions specify a
  different merge type), then tidy up — delete the remote and local branch,
  switch back to the base, and pull.
