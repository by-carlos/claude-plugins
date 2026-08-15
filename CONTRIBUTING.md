# Contributing

This repository is the **catalog** for the `carlos-plugins` marketplace. It
contains the marketplace manifest and its supporting files — no plugin code.

## Where to file things

- **A bug or idea about a plugin** → open it in that plugin's own repository,
  linked from [README.md](README.md). Issues opened here get transferred.
- **A bug about the catalog** → open it here: a plugin missing from the
  manifest, a source that won't resolve, a wrong description, a broken install
  command in the README.

## Workflow

1. **Open an issue first** for anything non-trivial. Typo fixes and other small
   changes can skip straight to a PR.
2. **Fork** the repo and branch off `main` (e.g. `fix/…`, `feat/…`, `docs/…`).
3. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/)
   (`feat:`, `fix:`, `docs:`, `chore:`, …) with clear, present-tense messages.
4. **Open a PR** against `main`. Keep it focused — one logical change per PR —
   and describe what changed and why.

The maintainer ([Carlos Eng](https://github.com/by-carlos)) reviews and merges
all PRs.

## Adding a plugin to the marketplace

A plugin is listed here only once it lives in its own public repository and
publishes a `release` branch. Add an entry to
`.claude-plugin/marketplace.json`:

```json
{
  "name": "<plugin-name>",
  "source": {
    "source": "github",
    "repo": "by-carlos/<repo>",
    "ref": "release"
  },
  "description": "<one line>"
}
```

Relative-path sources (`"source": "./some-dir"`) are rejected by CI — they
would resolve against whatever ref the marketplace clone sits at, which makes
every merge to `main` a release.

## Validation

A GitHub Actions workflow (`.github/workflows/validate.yml`) runs on every PR
and on pushes to `main`. It runs `scripts/validate_catalog.py`, which checks
that:

- `.claude-plugin/marketplace.json` parses and carries `name`, `owner` and a
  non-empty `plugins` list.
- Every plugin entry has a `name`, a `description` and a `source`.
- No entry uses a relative-path source.
- Every `github` source resolves — the repo exists and the `ref` is present,
  and the plugin's `.claude-plugin/plugin.json` is fetchable at that ref.
- Relative links in `README.md` resolve.

The script is stdlib-only Python (no external dependencies). Source resolution needs
network access and only covers repositories the run can see: a source that isn't
publicly visible is reported as a skip, not a failure. Set `GH_TOKEN` to resolve
private sources too. Run it locally before pushing:

```
python3 scripts/validate_catalog.py
```
