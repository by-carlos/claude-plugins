# Contributing

Thanks for your interest in improving these plugins. This is a small, solo-maintained
marketplace, so the workflow is deliberately lightweight.

## Workflow

1. **Open an issue first** for anything non-trivial — a bug, a new plugin idea, or a
   behavior change. It saves you from building something that won't be merged. Typo
   fixes and other small changes can skip straight to a PR.
2. **Fork** the repo and branch off `main` (e.g. `fix/…`, `feat/…`, `docs/…`).
3. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/)
   (`feat:`, `fix:`, `docs:`, `chore:`, …) with clear, present-tense messages.
4. **Open a PR** against `main`. Keep it focused — one logical change per PR — and
   describe what changed and why.

The maintainer ([Carlos Eng](https://github.com/by-carlos)) reviews and merges all PRs.

## Validation

A GitHub Actions workflow (`.github/workflows/validate.yml`) runs on every PR and on
pushes to `main`. It runs `scripts/validate_plugins.py`, which checks that:

- `.claude-plugin/marketplace.json` and each plugin's `.claude-plugin/plugin.json`
  parse as JSON, and every marketplace `source` path exists.
- `commands/*.md` have a `description` and `skills/*/SKILL.md` have `name` and
  `description` in their frontmatter.
- The templates referenced by each `SKILL.md` (`PLAN.md`, `LEDGER.md`, `stage-N.md`,
  `README.md`) exist under `references/templates/`.
- Relative links in `README.md` files resolve.

The script is stdlib-only Python (no external dependencies). Run it locally before
pushing:

```
python3 scripts/validate_plugins.py
```

## Ground rules

- Match the existing style and structure of the plugin you're touching.
- Update the relevant README and `CHANGELOG.md` when your change is user-facing.
- Be respectful and constructive — assume good faith on all sides.
