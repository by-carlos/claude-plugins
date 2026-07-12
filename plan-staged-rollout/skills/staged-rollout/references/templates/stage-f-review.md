# SF — Plan review

**depends:** <last stage(s)>  **mode:** direct  **exec:** inline  **model:** <model>  **effort:** <effort>

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md` — the *entire* ledger, every note, gotcha, shortcut, and
> known gap. This is the one stage exempt from the read-scope rule: read
> everything, not just what this stage depends on. Follow the protocol,
> including the finish protocol.

## Goal

Catalog every loose end the plan accumulated and close each one out. This
stage never implements — it only sorts findings into one of three outcomes
and records them.

## Steps

- [ ] Read every ledger row's notes end to end; list every loose end, gotcha,
  shortcut, and known gap surfaced across all stages.
- [ ] For each loose end, resolve it into exactly one outcome:
  - **New stage in this plan** — add a ledger row and a stage file; it runs
    later as a normal stage in its own fresh session and branch.
  - **Spin-off candidate** — record it in the ledger and note it for the
    final PR body as follow-up; it does not block closeout.
  - **Accepted, won't fix** — write a one-line reason in the ledger so the
    gap is a decision, not a surprise.
- [ ] Confirm no loose end was dropped: every item from the first step maps
  to exactly one of the three outcomes above.

<!-- Checkboxes are the resume mechanism: a session that stops mid-stage marks
the row `doing`, ticks the boxes it finished, and writes a handoff note in the
ledger. Re-running the stage resumes from the first unticked box. -->

## Acceptance

- Every loose end captured from the ledger is either a new ledger row (with
  a stage file) or explicitly closed (spin-off note or accepted-won't-fix
  reason) — paste the resulting list into the ledger notes as evidence.

## Artifacts

<Any new stage files or ledger rows this review spawned. No implementation
artifacts — this stage never builds anything itself.>
