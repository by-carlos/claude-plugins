# S4 — `/plan-run` command

**depends:** S2  **mode:** direct  **exec:** inline  **model:** opus  **effort:** med

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md` (incl. S2 notes). Follow the protocol, including the
> finish protocol. README sections to read: "How it works → 2. Execute".

## Goal

The runner: a thin wrapper that locates the project's `.plan/`, defers to the
protocol *inside that project's `PLAN.md`*, and adds the ergonomics (weight
check, resume, end announcement). It must NOT duplicate the protocol — the
scaffolded `PLAN.md` is the single source of truth and `.plan/` folders must
keep working without the plugin.

## Steps

- [ ] Write `commands/plan-run.md` with frontmatter (`description`,
      `argument-hint: <stage number>`).
- [ ] Flow: locate `.plan/` (error clearly if absent or the stage number
      doesn't match a stage file) → read the project `PLAN.md` protocol and
      follow it → weight check against the stage's `model`/`effort` flags
      (model verified, effort reminded; on mismatch warn + offer
      continue/abort) → dependency gate → resume support (if the stage is
      `doing`, continue from unticked checkboxes and the handoff note).
- [ ] End announcement: stage finished (or `blocked`/`doing` with what's
      pending), the next runnable stage — exact `/plan-run <N>` command — and
      its recommended model/effort; if no stages remain, point to
      `/plan-close`.

## Acceptance

- `commands/plan-run.md` exists, frontmatter parses, checklist review
  confirms the flow above.
- Grep-level check: the command contains no copy of the operating protocol
  steps (it defers to the project's `PLAN.md`). Live behavior verified in S6.

## Artifacts

`plan-staged-rollout/commands/plan-run.md`
