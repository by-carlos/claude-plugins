# <Project name> — plan & protocol

<One-paragraph statement of what this project builds and why. If a longer
design narrative exists, point at it here and keep this file as the executable
spec.> This file is the **single source of truth** for durable decisions: the
architecture, the frozen decisions, the stage index, and the operating
protocol every stage session follows. Decisions live here and are *referenced,
never copied* — a decision that exists in one place cannot diverge.

## Architecture (what we're building)

```
<Sketch the target layout / components here — the shape the finished work
takes. Keep it current; amend it when a stage changes the design.>
```

## Frozen decisions

Change these in THIS file only — never restate them in stage files or the
ledger. If a stage changes a decision, amend it here as the last step of that
stage (Operating protocol, finish step 3).

- <Decision 1 — e.g. naming, key library/tool choice, a hard constraint.>
- <Decision 2.>
- **Git strategy:** branch-per-stage (default). `main` → `plan-<slug>` (the
  plan branch; `.plan/` lives here) → one branch per stage
  `plan-<slug>-s<N>` (flat names — git refs can't nest a branch under an
  existing branch), each landing as a PR into `plan-<slug>`; final PR
  `plan-<slug>` → `main` at closeout. The agent creates and pushes stage and
  plan branches without asking, then offers the stage PR (and its merge) for
  your OK — it never merges on its own and never pushes to `main`. <Replace
  this bullet if you chose an alternative at bootstrap:
  single plan branch with direct commits, or plain trunk.>
- **Final review stage:** the last stage (`SF`) is a standing plan review. It
  catalogs loose ends — each becomes a new in-plan stage, a spin-off
  candidate, or an explicit "accepted, won't fix" — and NEVER implements.

## Stage index & dependencies

| Stage | File | Depends | mode | exec | model | effort |
|---|---|---|---|---|---|---|
| S0 <keystone stage — the piece everything needs> | `stage-0-<slug>.md` | — | direct | inline | <model> | <effort> |
| S1 <stage name> | `stage-1-<slug>.md` | S0 | direct | inline | <model> | <effort> |
| ... | ... | ... | ... | ... | ... | ... |
| SF Plan review | `stage-f-review.md` | <last impl stage> | direct | inline | <model> | <effort> |

Flag values: `mode` = `direct` \| `brainstorm`; `exec` = `inline` \|
`subagent(<model>)`; `model`/`effort` = launch hints (checked, not faked).
Defaults are deliberately cheap — `direct`, `inline`, the cheaper capable
model. Escalate only where a stage has genuine open design questions
(`brainstorm`) or heavy iteration churn (`subagent`).

## Operating protocol (every stage session)

1. **Read only:** this file + the target stage file + the `LEDGER.md` status
   table + the notes blocks of the stages this one `depends` on + any docs the
   stage file names. Do NOT scan the rest of the repo. (Exception: the final
   review stage reads the *entire* ledger.)
2. **Weight check:** compare the session's model against the stage's `model`
   flag (your system prompt states your model); remind the recommended
   `effort` — effort is NOT introspectable, so never claim to verify it. If
   the session is lighter than recommended, say so and offer continue/abort
   before doing anything.
3. **Dependency gate:** for every `depends` stage, confirm it is `done` in
   `LEDGER.md` **AND its stage branch/PR is merged into the plan branch**
   (`git fetch` first — the merge may be remote and not yet local). Both must
   hold. A `done` ledger row alone is not enough: a stage branched off the
   plan branch before a prerequisite's PR is merged will silently lack that
   prerequisite's work. If either isn't true, stop and say so.
4. **Branch:** first make sure the local plan branch is up to date
   (`git fetch` + fast-forward), then create `plan-<slug>-s<N>` from
   `plan-<slug>` (or use it if the human already made it). Work
   happens on the stage branch. <Adjust if you chose a non-default git
   strategy.>
5. **Honor `mode` / `exec`:**
   - `mode: direct` → state a one-line plan, then implement.
   - `mode: brainstorm` → run a design pass scoped to THIS stage first,
     treating frozen decisions as settled; land outcomes as frozen decisions
     here, not in a second spec.
   - `exec: inline` → implement in this session.
   - `exec: subagent(<model>)` → act as orchestrator and dispatch the
     implementation to a subagent so the churn stays out of this context.
6. **Scope discipline:** do only this stage. Work belonging to another stage →
   note it in the ledger notes and leave it untouched. It may become a new
   stage.
7. **Finish protocol (required):**
   1. Run the stage's **Acceptance** checks; paste the real output into the
      stage's notes block in `LEDGER.md`.
   2. Update the stage's table row: status, absolute date, verified yes/no,
      one-line result. Detail goes in the notes block, never the table.
   3. If a decision changed or was added, amend **Frozen decisions in this
      file** — nowhere else.
   4. Commit on the stage branch (conventional message) and **push it**, then
      **offer** to open the PR into `plan-<slug>` and to merge it once
      reviewed — never merge on your own.
   5. Announce: this stage is **finished**; the next runnable stage (the first
      `todo` whose `depends` are all `done`), the exact prompt/command to run
      it, and its recommended model/effort. Then stop.
