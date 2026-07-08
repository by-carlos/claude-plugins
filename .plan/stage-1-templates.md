# S1 — Scaffold templates

**depends:** S0  **mode:** direct  **exec:** inline  **model:** opus  **effort:** med

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md`. Follow the protocol, including the finish protocol.
> README sections to read: "How it works" (all of it), "Per-stage knobs",
> "The ledger, kept slim".

## Goal

The four files `/plan-stages` copies when scaffolding a project's `.plan/` —
these templates ARE the method as experienced by users, so they carry the
ledger diet, checkbox steps, flags, and the full operating protocol.

## Steps

- [ ] `references/templates/PLAN.md` — architecture, frozen decisions, stage
      index (with `depends`/`mode`/`exec`/`model`/`effort` columns), and the
      complete operating protocol: read-scope, weight check (model verified /
      effort reminded), dependency gate, stage-branch step, mode/exec, scope
      discipline, finish protocol ending with the "announce finished + next
      command + model/effort" step.
- [ ] `references/templates/LEDGER.md` — one-line status table
      (`Stage | Status | Verified | Date | Result`) + per-stage `### S<N>`
      notes blocks; header states the one-line-row rule and the read-scope
      rule.
- [ ] `references/templates/stage-N.md` — flags header, the "first read
      PLAN.md/LEDGER.md" pointer, Goal, checkbox Steps, Acceptance (must
      produce pasteable evidence), Artifacts.
- [ ] `references/templates/README.md` — project-facing entry point: the
      one-line runner prompt, `/plan-run <N>` usage, file map, git model
      summary.
- [ ] Cross-check against the pilot (`C:\GitHub\linux\.plan`, read-only): the
      templates must cover everything the pilot needed (blocked/runbook
      stages, follow-up stages, frozen-decision amendments) while fixing its
      known flaw (notes crammed into table cells).

## Acceptance

- All four templates exist; placeholder slots use a single consistent style
  (`<angle-brackets>`).
- Internal consistency check passes: statuses, table columns, file names, and
  flag names are identical across all four templates and match the frozen
  decisions in `.plan/PLAN.md`.
- No pilot-specific (homelab/logging) content leaked into the templates.

## Artifacts

`plan-staged-rollout/skills/staged-rollout/references/templates/{PLAN,LEDGER,stage-N,README}.md`
