---
description: Bootstrap a staged-rollout .plan/ from a project idea — design, decompose, scaffold, and commit. Executes no stage.
argument-hint: <project idea>
---

# /plan-stages — bootstrap a `.plan/` scaffold

Turn a project idea into a committed `.plan/` folder: design → decompose →
scaffold → commit. **No stage is executed here.** This command is a thin
wrapper around the `staged-rollout` skill; the skill and its
`references/templates/` are the single source of truth for the method and file
formats. Do not restate the protocol here or in the scaffold — reference it.

Project idea: **$ARGUMENTS**

First, load the method: invoke the **`staged-rollout`** skill (via the Skill
tool) and follow its decomposition guidance, flag heuristics, and git model.
The templates to copy live at
`${CLAUDE_PLUGIN_ROOT}/skills/staged-rollout/references/templates/`
(`PLAN.md`, `LEDGER.md`, `stage-N.md`, `stage-f-review.md`, `README.md`).

Then work through these steps **in order**:

1. **Weight gate (first, before anything else).** Bootstrap is the
   highest-leverage session of a plan. Verify from your own system prompt that
   the session model is **Opus-class or better**, checked mechanically against
   the skill's **Model weight tiers** rubric — not the model's own guess about
   itself. State the effort recommendation (**medium or higher**) as a
   reminder — effort is not introspectable, so never claim to verify it. If
   the model is lighter than Opus-class, warn and **offer to abort** so the
   user can relaunch on a heavier model, before doing any design or
   scaffolding work. If the disclosed model doesn't recognizably match a tier
   in the rubric, don't guess — state the exact model ID/name and ask the
   user which tier applies.

2. **Design pass (only if the design isn't already settled).** If `$ARGUMENTS`
   already carries settled decisions, skip straight to decomposition. Otherwise
   run a design pass: use **`superpowers:brainstorming`** when it is installed;
   else fall back to a built-in lightweight flow — **one question at a time,
   multiple-choice preferred**, converging on the decisions worth freezing.
   Outcomes land **directly as Frozen decisions in the scaffolded `PLAN.md`** —
   never as a separate spec document (a second source of truth is exactly what
   this method exists to prevent).

3. **Decompose.** Apply the skill's guidance: smallest sensible stages, explicit
   `depends`, the keystone as **S0**, and deliberately cheap flags (`direct`,
   `inline`, the cheaper capable model — escalate only where a stage genuinely
   warrants it). Then **append the standing `SF: plan review` stage** as the
   last row (it catalogs loose ends and never implements), scaffolded from
   `stage-f-review.md` — not a copy of `stage-N.md` — since it already bakes
   in the three-outcome checklist and acceptance check.

4. **Git model (fixed, not a question).** Record the frozen git protocol in
   `PLAN.md`: **branch-per-stage** — `main` → `plan-<slug>` (the plan branch)
   → one `plan-<slug>-s<N>` branch and PR per stage, no exceptions, final PR
   to `main` at closeout. It is the only supported model — do not ask the
   user to choose. Six frozen semantics: (1) one branch per stage, cut from
   the plan branch; (2) commits are compulsory and incremental — commit at
   logical units as the stage progresses, not once at the end; (3) a stage PR
   into the plan branch is compulsory — the finish protocol creates it, it is
   not offered; (4) a stage cannot be marked `done` until its PR is merged
   into the plan branch; (5) after the merge, check out the plan branch and
   fast-forward before the session ends; (6) merge type is fixed by position —
   stage PRs are **squash-merged** into the plan branch (merged branch
   deleted), and the final PR from the plan branch into `main` is a **normal
   (non-squash) merge** so each stage keeps its own commit on `main`. Do
   **not** create any *stage* branch
   here — stage branches (`plan-<slug>-s<N>`) are proposed and created at
   stage time by `/plan-staged-rollout:plan-run`, never at bootstrap.

5. **Scaffold and commit.** Copy the templates into `<repo>/.plan/`, copying
   `stage-N.md` **once per stage** and renaming each to `stage-<N>-<slug>.md`,
   and copying `stage-f-review.md` **once**, renamed to `stage-f-review.md`
   (no slug needed — it's the standing final stage), and fill every
   placeholder (frozen decisions, stage index, ledger rows, per-stage files).
   Then land the scaffold on the plan branch: **propose
   creating the plan branch `plan-<slug>` off `main`** and put the scaffold
   there — `.plan/` lives on the plan branch. **Propose the scaffold commit**
   (conventional message, e.g. `chore(plan): scaffold .plan/ for <slug>`) and
   wait for the user's OK — do not create the branch or commit unilaterally.

6. **End announcement.** State explicitly that **bootstrap is finished and no
   stage was executed.** Tell the user their next action, in a **fresh
   session**, is **"run stage 0 of the plan"** — or the explicit command
   **`/plan-staged-rollout:plan-run 0`** — and state **S0's recommended model
   and effort** from the stage index. Then stop.
