# S6 — End-to-end dogfood test

**depends:** S3, S4, S5  **mode:** direct  **exec:** inline  **model:** opus  **effort:** med

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md` (incl. S3, S4, S5 notes). Follow the protocol, including
> the finish protocol. README sections to read: "How it works" (all).

## Goal

Prove the plugin actually behaves as the README promises, on a throwaway
project, with real evidence — and fix what doesn't.

## Steps

- [ ] Install the plugin locally (add this repo as a local marketplace /
      `--plugin-dir`, whichever the current CLI supports — verify against
      docs) and confirm the skill and all three commands are listed.
- [ ] Create a throwaway git repo with a small toy project idea (e.g., a
      3–4 stage CLI utility) outside this repo.
- [ ] Run `/plan-stages <toy idea>`: verify the weight gate fires, the design
      pass triggers (or is skipped when the design is given as settled), the
      scaffold matches the templates (PLAN.md protocol present, ledger split
      correct, S-final appended, git strategy recorded), no stage was
      executed, and the end announcement names `/plan-run 0` with
      model/effort.
- [ ] Run `/plan-run 0` end-to-end: weight check, dependency gate, checkbox
      steps, acceptance evidence pasted, ledger row + notes updated, stage
      branch/PR proposed, end announcement names the next stage.
- [ ] Run `/plan-run` on a stage whose `depends` isn't done: verify the gate
      refuses.
- [ ] Run `/plan-close` with stages pending: verify it refuses and lists the
      pending stages.
- [ ] Fix any defects found in the commands/templates/skill (in scope for
      this stage — they're the deliverable under test); note anything larger
      in the ledger for SF.

## Acceptance

- Pasted transcript evidence in the ledger notes for each verification above
  (scaffold listing, gate refusals, end announcements).

## Artifacts

Fixes to `plan-staged-rollout/` files as needed; evidence in `LEDGER.md`
notes. The toy repo is throwaway — do not commit it here.
