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
