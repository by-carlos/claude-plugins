# Build the `plan-staged-rollout` plugin — plan & protocol

The full method and design narrative live in `plan-staged-rollout/README.md`
(the design doc distilled from the 2026-07-08 design session). This file is
the executable spec for *building the plugin*: frozen decisions, stage index,
and the operating protocol every stage session follows. If a decision here
ever conflicts with the README, THIS file wins during the build; the review
stage (SF) reconciles the README before closeout.

## Architecture (what we're building)

```
plan-staged-rollout/
  .claude-plugin/plugin.json     # plugin manifest
  README.md                      # showcase + design doc (exists)
  skills/staged-rollout/
    SKILL.md                     # method: principles, decomposition guidance,
                                 #   flag heuristics, anti-patterns
    references/templates/        # PLAN.md, LEDGER.md, stage-N.md, README.md
  commands/
    plan-stages.md               # /plan-stages <idea>  — bootstrap a .plan/
    plan-run.md                  # /plan-run <N>        — execute one stage
    plan-close.md                # /plan-close          — final PR + cleanup
```

## Frozen decisions

Change these in THIS file only — never restate them in stage files.

- Plugin dir/name: `plan-staged-rollout`. Skill name: `staged-rollout`.
- Commands: `/plan-stages <idea>`, `/plan-run <N>`, `/plan-close`.
- Source-of-truth file in scaffolded projects is named **`PLAN.md`**.
- The operating protocol lives in each scaffolded project's `PLAN.md`, not in
  the plugin — `.plan/` folders must work standalone via the one-line prompt
  "Follow the instructions in `.plan/stage-N-<slug>.md`". Commands are thin
  ergonomic wrappers and must NOT duplicate the protocol.
- Ledger split: strict one-line status table
  (`Stage | Status | Verified | Date | Result`) + per-stage `### S<N>` notes
  blocks. Read-scope = table + notes of `depends` stages only.
- Statuses: `todo / doing / done / blocked / skipped`.
- Stage steps are checkboxes; mid-stage stop = mark `doing`, tick boxes,
  handoff note; re-run resumes from unticked boxes.
- Git default (and the model used for THIS build): plan branch + one branch
  per stage (`<planbranch>-s<N>`, flat names — git refs can't nest under an
  existing branch) + PR into the plan branch, **no exceptions per stage**;
  final PR plan branch → `main` at closeout. Alternatives offered only at
  bootstrap: single plan branch (infra-style) or trunk.
- Agent proposes every branch/PR/merge/push and waits for Carlos's OK; it
  never merges or pushes on its own.
- `/plan-stages` gates on session weight: model must be Opus-class or better
  (verified from the session); effort medium+ is a stated reminder — effort
  is NOT introspectable, never claim to verify it. `/plan-run` verifies model
  and reminds effort against the stage's flags; on mismatch, warn and offer
  continue/abort.
- Every command ends by explicitly stating it is finished, what the user runs
  next (exact command), and the recommended model/effort for it.
- Bootstrap always appends a standing final review stage; the review stage
  catalogs (new stage in-plan / spin-off candidate / accepted-won't-fix) and
  NEVER implements. `/plan-close` refuses until all rows are done/skipped,
  distills PLAN.md + ledger into the final PR body, deletes `.plan/` as the
  last commit (keeping it is an offered option), proposes the PR to main.
- Design-pass dependency is soft: use `superpowers:brainstorming` when
  installed, else a built-in lightweight one-question-at-a-time fallback.
  Decisions land as frozen decisions in `PLAN.md`, never a second spec doc.
- `plan-staged-rollout/plan-staged-rollout.prompt.md` is absorbed into
  SKILL.md + templates and deleted in S2 (content survives in git history).
- Deferred (roadmap, do NOT build now): subagent fan-out for sub-steps,
  parallel stage execution, `next-stage` helper script, progress dashboard,
  skill evals.
- Pilot reference (read-only, for cross-checking templates):
  `C:\GitHub\linux\.plan`.

## Stage index & dependencies

| Stage | File | Depends | mode | exec | model | effort |
|---|---|---|---|---|---|---|
| S0 Plugin scaffold & manifest | `stage-0-scaffold.md` | — | direct | inline | sonnet | low |
| S1 Scaffold templates | `stage-1-templates.md` | S0 | direct | inline | opus | med |
| S2 SKILL.md | `stage-2-skill.md` | S0, S1 | direct | inline | opus | med |
| S3 `/plan-stages` command | `stage-3-plan-stages-cmd.md` | S1, S2 | direct | inline | opus | med |
| S4 `/plan-run` command | `stage-4-plan-run-cmd.md` | S2 | direct | inline | opus | med |
| S5 `/plan-close` command | `stage-5-plan-close-cmd.md` | S2 | direct | inline | sonnet | med |
| S6 End-to-end dogfood test | `stage-6-dogfood.md` | S3, S4, S5 | direct | inline | opus | med |
| SF Plan review | `stage-f-review.md` | S6 | direct | inline | opus | med |

## Operating protocol (every stage session)

1. **Read only:** this file + the target stage file + the `LEDGER.md` status
   table + the notes blocks of the stages this one `depends` on + the
   `plan-staged-rollout/README.md` sections the stage file lists. Do NOT scan
   the rest of the repo or re-read the whole README.
2. **Weight check:** compare the session's model against the stage's `model`
   flag (the system prompt states your model); remind the recommended
   `effort` (you cannot verify it). If the session is lighter than
   recommended, say so and offer continue/abort before doing anything.
3. **Dependency gate:** for every `depends` stage, confirm it is `done` in
   `LEDGER.md` **AND its stage branch/PR is merged into the plan branch**
   (`git fetch` first — the merge may be remote and not yet local). Both must
   hold. A `done` ledger row alone is not enough: a stage branched off the
   plan branch before a prerequisite's PR is merged will silently lack that
   prerequisite's work. If either isn't true, stop and say so.
4. **Branch:** first make sure the local `plan-staged-rollout` branch is up to
   date (`git fetch` + fast-forward), then propose creating
   `plan-staged-rollout-s<N>` from `plan-staged-rollout` and wait for Carlos's
   OK (he may create it himself). Work happens on the stage branch.
5. **Honor `mode`/`exec`** (all stages here are `direct`/`inline`: state a
   one-line plan, implement — no brainstorming pass, no subagents).
6. **Scope discipline:** do only this stage. Work belonging to another stage
   → note it in the ledger notes and leave it untouched.
7. **Finish protocol (required):**
   1. Run the stage's **Acceptance** checks; paste the real output into the
      stage's notes block in `LEDGER.md`.
   2. Update the stage's table row: status, absolute date, verified yes/no,
      one-line result. Detail goes in the notes block, never the table.
   3. If a decision changed or was added, amend **Frozen decisions in this
      file** — nowhere else.
   4. Commit on the stage branch (conventional message), then propose the PR
      into `plan-staged-rollout` and wait for Carlos.
   5. Announce: this stage is **finished**; the next runnable stage (first
      `todo` whose `depends` are all `done`), the exact prompt/command to run
      it, and its recommended model/effort. Stop.
