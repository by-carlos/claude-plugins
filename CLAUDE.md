# CLAUDE.md — claude-plugins

Project instructions for agentic coding in this repository.

## Git & merge conventions

- **Merge strategy:** Default to **squash merge** for pull requests, unless a
  plugin/skill/workflow in this repo specifies a different merge type, or the
  maintainer asks for one.
- **Branch cleanup:** After a branch is merged, **delete it** by default to keep
  the branch list tidy — unless the workflow says to keep it or the maintainer
  asks otherwise.
- **Exception — staged rollouts:** the `plan-staged-rollout` plugin defines its
  own merge model that overrides the squash default for the final integration.
  Stage PRs into the plan branch (`plan-<slug>`) are **squash-merged**; the final
  PR from the plan branch into `main` is a **normal (non-squash) merge**, so each
  stage lands as a distinct commit on `main`. See
  [plan-staged-rollout/skills/staged-rollout/SKILL.md](plan-staged-rollout/skills/staged-rollout/SKILL.md).
- Merging is never unilateral: propose the merge and wait for the maintainer's OK.
  Never push directly to `main`.

## Secret scanning

[gitleaks](https://github.com/gitleaks/gitleaks) runs in CI on every push/PR
([`.github/workflows/gitleaks.yml`](.github/workflows/gitleaks.yml)); known
historical findings would be baselined in
[`.gitleaks-baseline.json`](.gitleaks-baseline.json) (currently empty — clean
history) so CI stays green on dead history while still catching anything new.
No local pre-commit hook — dev environments vary, so this is CI-only by design.

## Releasing

- **`main` is live distribution.** The marketplace source tracks the branch, not a
  tag — so anything merged to `main` reaches any user who refreshes the marketplace
  (`/plugin marketplace update`), regardless of version bump or GitHub release. A
  release is a human-facing label, not the delivery mechanism. Keep `main` releasable.
- **Changelog as-you-go, under `## [Unreleased]`.** Add entries to `CHANGELOG.md`
  under an `## [Unreleased]` heading as changes land. This records *what* changed
  without declaring a version. Never write a dated/versioned heading or bump
  `plugin.json` mid-batch — that recreates version drift.
- **A release is one atomic change**, done all together (own commit/PR):
  1. Bump `version` in the affected plugin's `.claude-plugin/plugin.json` (semver).
  2. Rename `## [Unreleased]` → `## [x.y.z] — YYYY-MM-DD` and add the
     `[x.y.z]: …/releases/tag/vx.y.z` link at the bottom.
  3. Tag `vx.y.z` and cut the matching GitHub release.
- **Semver:** a `feat` in the batch ⇒ **minor** bump; only `fix`/`docs`/`chore` ⇒
  **patch**. Pre-1.0, breaking changes go in a minor.
- **Tag per released version** (not per commit, not major-only) — the `CHANGELOG.md`
  release links assume a tag exists for each version. Keep the two consistent.
