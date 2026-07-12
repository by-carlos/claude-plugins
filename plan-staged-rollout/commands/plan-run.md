---
description: Execute one stage of a staged-rollout .plan/ — locate the stage, follow the project's own PLAN.md protocol, verify launch weight, and hand off to the next stage.
argument-hint: <stage number, or f for the review stage>
---

# /plan-run — execute one stage

Run a single stage of an existing `.plan/`. This command is a **thin wrapper**:
the operating protocol lives in the project's own `.plan/PLAN.md`, so a `.plan/`
works standalone via the one-line prompt "Follow the instructions in
`.plan/stage-N-<slug>.md`". Do **not** restate or duplicate that protocol here —
locate the stage, defer to `PLAN.md`, and add only the ergonomics below.

Stage to run: **$ARGUMENTS**

Work through these steps **in order**:

1. **Locate `.plan/`.** Find the `.plan/` directory at the repo root. If none
   exists, stop and tell the user to bootstrap one — "bootstrap a plan for
   \<idea>", or the explicit command `/plan-staged-rollout:plan-stages <idea>`.
   Then resolve `$ARGUMENTS` to the stage file `.plan/stage-<N>-<slug>.md` by
   matching the leading `stage-<$ARGUMENTS>-` token — a digit for an
   implementation stage, or `f` for the final review stage
   (`stage-f-review.md`). If nothing matches, stop and list the stage files that
   do exist so the user can pick a valid one.

2. **Defer to the project protocol.** Read `.plan/PLAN.md` and follow its
   **Operating protocol** verbatim for this stage — read-scope, dependency gate,
   `mode`/`exec` handling, scope discipline, and the finish protocol all come
   from that file, not from this command. `PLAN.md` is the single source of
   truth; this wrapper never overrides it.

3. **Weight check (ergonomic add).** Before doing any stage work, compare the
   session against the stage's `model` and `effort` flags in `.plan/PLAN.md`'s
   stage index. Verify the **model** from your own system prompt, checked
   mechanically against the `staged-rollout` skill's **Model weight tiers**
   rubric — not a guess about your own weight. State the recommended
   **effort** as a reminder only — effort is not introspectable, so never
   claim to verify it. If the session is **lighter** than the stage
   recommends, say so plainly and **offer continue or abort** so the user can
   relaunch on a heavier session before any work begins. If the disclosed
   model doesn't recognizably match a tier in the rubric, don't guess — state
   the exact model ID/name and ask the user which tier applies.

4. **Dependency gate (ergonomic surfacing of the protocol's rule).** Apply
   `PLAN.md`'s dependency gate for every stage this one `depends` on. If a
   prerequisite is not satisfied, stop and say exactly which one and why — do
   not start the stage.

5. **Resume support.** Check the stage's ledger status in `.plan/LEDGER.md`. If
   it is already `doing`, this is a resume: pick up from the **unticked**
   checkboxes in the stage file's Steps and honor the handoff note in the
   stage's ledger notes block. If it is `done`, confirm with the user before
   redoing anything. Otherwise run it fresh.

6. **End announcement.** When you stop, state explicitly:
   - The stage's outcome: **finished**, or `blocked`/`doing` — and if not
     finished, exactly what remains (which checkboxes, what it's waiting on).
   - The **next runnable stage**: the first `todo` stage whose `depends` are all
     `done`. Tell the user to continue in a fresh session with **"run stage
     \<N> of the plan"** — or the explicit command
     **`/plan-staged-rollout:plan-run <N>`** — and state its recommended
     **model and effort** from the stage index.
   - If no stages remain runnable (all `done`/`skipped`), point the user at
     closeout — **"close out the plan"** or **`/plan-staged-rollout:plan-close`**
     — instead.
   Then stop.
