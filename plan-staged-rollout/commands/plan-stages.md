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
(`PLAN.md`, `LEDGER.md`, `stage-N.md`, `README.md`).

Then work through these steps **in order**:

1. **Weight gate (first, before anything else).** Bootstrap is the
   highest-leverage session of a plan. Verify from your own system prompt that
   the session model is **Opus-class or better**. State the effort
   recommendation (**medium or higher**) as a reminder — effort is not
   introspectable, so never claim to verify it. If the model is lighter than
   Opus-class, warn and **offer to abort** so the user can relaunch on a
   heavier model, before doing any design or scaffolding work.

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
   last row (it catalogs loose ends and never implements).

4. **Git strategy question.** Ask the user which model to use. **Default:
   branch-per-stage** — `main` → `plan-<slug>` → one `plan-<slug>-s<N>` branch
   and PR per stage, no per-stage exceptions, final PR to `main` at closeout.
   Offer the alternatives: **single plan branch** (direct commits — infra-style
   rollouts) or **trunk**. Record the choice as a **frozen decision** in
   `PLAN.md`. Do **not** create any *stage* branch here — stage branches
   (`plan-<slug>-s<N>`) are proposed and created at stage time by `/plan-run`,
   never at bootstrap.

5. **Scaffold and commit.** Copy the four templates into `<repo>/.plan/`, copying
   `stage-N.md` **once per stage** and renaming each to `stage-<N>-<slug>.md`,
   and fill every placeholder (frozen decisions, stage index, ledger rows,
   per-stage files). Then land the scaffold on the plan branch: unless the chosen
   strategy is **trunk**, **propose creating the plan branch `plan-<slug>` off
   `main`** and put the scaffold there — `.plan/` lives on the plan branch (for
   trunk, it stays on the current branch). **Propose the scaffold commit**
   (conventional message, e.g. `chore(plan): scaffold .plan/ for <slug>`) and
   wait for the user's OK — do not create the branch or commit unilaterally.

6. **End announcement.** State explicitly that **bootstrap is finished and no
   stage was executed.** Tell the user their next action is **`/plan-run 0`** in
   a **fresh session**, and state **S0's recommended model and effort** from the
   stage index. Then stop.
