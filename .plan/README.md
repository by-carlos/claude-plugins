# `.plan/` — building the `plan-staged-rollout` plugin

Ledger-driven, one-stage-at-a-time build of the plugin itself — the method
dogfooding itself. Designed for short, fresh, resumable sessions.

## Run a stage

Start a fresh Claude Code session **on the model/effort the stage recommends**
(see the stage index in `PLAN.md`) and paste one line:

> Follow the instructions in `.plan/stage-0-scaffold.md`.

That's the whole prompt. The stage file redirects to the shared protocol and
frozen decisions in `PLAN.md`, checks `LEDGER.md`, does the work, verifies it,
updates the ledger, and proposes the stage PR. Next session, point at the next
stage file. (The `/plan-run` command this plan builds will replace the manual
prompt — for this build, S0–S5 run manually; S6 onward can dogfood the
commands.)

## Files

- `PLAN.md` — frozen decisions, stage index, operating protocol. Source of
  truth for the build.
- `LEDGER.md` — status table + per-stage notes. The only file every session
  mutates.
- `stage-*.md` — one small, self-contained stage each.

## Git

Plan branch: `plan-staged-rollout` (already checked out). Each stage works on
`plan-staged-rollout-s<N>` and PRs back into the plan branch; the final PR to
`main` happens at closeout. Branch/PR/merge/push are proposed to Carlos, never
executed unilaterally. Once SF is done, closeout can dogfood `/plan-close` on
this very plan.
