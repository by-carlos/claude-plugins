# `.plan/` — <Project name>

Ledger-driven, one-stage-at-a-time rollout, built to run in **short,
low-context sessions you can pick up whenever you have time**. Each stage runs
in its own fresh session and lands as its own PR, so context never accumulates
and any single stage is easy to review or undo.

## How to run a stage

Start a **fresh** session and paste one line:

> Follow the instructions in `.plan/stage-<N>-<slug>.md`.

That's the whole prompt — the stage file points the session at the shared
protocol and frozen decisions in `PLAN.md`. If this repo has the
`plan-staged-rollout` plugin installed, `/plan-run <N>` is the same thing with
ergonomics (it also runs the model/effort weight check for you). The `.plan/`
folder works standalone either way; the plugin is convenience, not a
dependency.

Run stages in any order allowed by their `depends`. The next runnable stage is
the first `todo` row in `LEDGER.md` whose dependencies are all `done`.

## Files

- `PLAN.md` — architecture, **frozen decisions**, stage index, and the
  operating protocol every stage session follows. Single source of truth for
  decisions; changed only when a decision changes.
- `LEDGER.md` — status table + per-stage as-built notes. The tracker that
  changes as you execute; the resume point and cross-session memory.
- `stage-<N>-<slug>.md` — one small, self-contained stage each.

## Git model

```
main
 └── plan-<slug>                    ← plan branch; .plan/ lives here
      ├── plan-<slug>-s0  → PR → plan-<slug>
      ├── plan-<slug>-s1  → PR → plan-<slug>
      └── ...
plan-<slug> → final PR → main       ← at /plan-close
```

Every stage gets its own branch and PR into the plan branch. Branch names are
flat (`plan-<slug>-s3`, not `plan/<slug>/s3`) because git refs can't nest a
branch under an existing branch name. Branch creation, PRs, and merges are
always proposed and executed on your acceptance — the agent never merges or
pushes on its own. <If you chose a non-default git strategy at bootstrap
(single plan branch, or trunk), describe it here instead.>

## Closeout

When every ledger row is `done` or `skipped`, run `/plan-close` (or follow the
closeout steps in `PLAN.md`): it distills `PLAN.md` + the ledger into the final
PR body, deletes `.plan/` as the last commit (keeping it is an option), and
proposes the PR from `plan-<slug>` to `main`.
