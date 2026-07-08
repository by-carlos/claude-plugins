# SF — Plan review

**depends:** S6  **mode:** direct  **exec:** inline  **model:** opus  **effort:** med

> First read `.plan/PLAN.md` and ALL of `.plan/LEDGER.md` — this is the one
> stage exempt from the read-scope rule: read every stage's notes.

## Goal

Sweep the whole build for loose ends and reconcile the docs. Catalog only —
this stage NEVER implements.

## Steps

- [ ] Read every notes block in the ledger; list every loose end, shortcut,
      gotcha, and deferred item mentioned anywhere.
- [ ] Convert each finding into exactly one of: a new stage in this plan
      (ledger row + stage file, runs later in its own session/branch), a
      spin-off candidate (recorded for the final PR body; future
      `/plan-stages` project), or an explicit "accepted, won't fix" with a
      one-line reason.
- [ ] Reconcile `plan-staged-rollout/README.md` with `.plan/PLAN.md`: any
      frozen decision amended during the build must be reflected in the
      README (PLAN.md won during the build; the README must not ship stale).
- [ ] Verify every `done` row has acceptance evidence in its notes block;
      flag any that don't as new findings.
- [ ] Check the roadmap section of the README still matches reality
      (deferred items neither silently built nor silently dropped).

## Acceptance

- Every loose end found in the notes is either a new ledger row or explicitly
  closed — none left uncategorized (list them with their resolution).
- README and PLAN.md agree; grep for the old command names
  (`plan-new`, `stage-run`, `stage-plan`) returns nothing.

## Artifacts

Updated `LEDGER.md` (+ any new stage files), reconciled README. After this
stage and any stages it spawned are done, close the plan — dogfooding
`/plan-close` on this very `.plan/`.
