# Plan-Driven Staged Rollout — Reusable Method

A repeatable way to take a **large, multi-step build** and execute it across
**many short sessions** without (a) blowing up context/token cost, (b) letting
the design drift as it evolves, or (c) losing your place between sessions. It
uses a small set of Markdown files in a `.plan/` folder plus a one-line reusable
prompt.

> **This document is solution-agnostic and self-contained.** It describes the
> *approach* only. It was distilled from a real build (a homelab logging rollout)
> but nothing here is specific to that domain. Use it to scaffold any staged
> project. It's written to be turned into a skill — see §12.

---

## 1. When to use this

Reach for this method when **all** of these are true:

- The work is **big enough to span multiple sessions** (hours/days, not one turn).
- It **decomposes into a sequence of smaller units** with some ordering/dependencies.
- You want to **stop and resume freely** ("do a bit when I have time").
- You care about **keeping token cost and context small** per session.
- The **design will evolve** as you learn things mid-build, and you need it not to
  drift into contradictory copies.

Don't use it for a single-session task, or work that can't be decomposed.

---

## 2. Core principles (the "why")

Everything below follows from four ideas:

1. **One source of truth, referenced not copied.** All durable decisions live in
   exactly one file (`DESIGN.md`). Stage files and prompts *point at it*; they
   never restate its contents. Copies are what drift — if a decision exists in one
   place, it cannot diverge.

2. **Small stages + fresh session per stage = free context control.** The primary
   token-control mechanism isn't subagents or clever prompting — it's that each
   stage is small and runs in its own fresh session, so context never accumulates
   across stages. A one-line config change in a clean session stays cheap.

3. **The ledger is the resume point *and* the memory.** A single mutable
   `LEDGER.md` holds per-stage status and **detailed as-built notes**. You resume
   by reading it and picking the next unstarted stage. The notes also let a later
   stage catch a regression an earlier stage introduced (because the earlier
   stage's assumptions are written down).

4. **Verify before you claim done.** A stage isn't done because the model says so
   — it's done when its **acceptance check runs and the real output is pasted into
   the ledger.** Evidence, not assertion.

---

## 3. What you produce: the `.plan/` folder

```
<repo>/.plan/
  README.md      # human entry point + the one-line runner prompt
  DESIGN.md      # SINGLE SOURCE OF TRUTH: architecture, frozen decisions,
                 #   stage index (with per-stage flags), operating protocol
  LEDGER.md      # mutable progress tracker + detailed as-built notes
  stage-0-<slug>.md
  stage-1-<slug>.md
  ...            # one small, self-contained stage per file
```

Create it on a **dedicated branch** so the plan and the work it produces are
isolated until you're ready to integrate.

Rule of thumb for the split:
- `DESIGN.md` changes **rarely** (only when a decision changes).
- `LEDGER.md` changes **every session** (it's the only thing execution mutates).
- `stage-*.md` are written once up front and stay **thin**.

---

## 4. The reusable runner prompt

This is the whole thing you paste into a fresh session to execute a stage:

> **Follow the instructions in `.plan/stage-<N>-<slug>.md`.**

That's it. The stage file redirects the agent to read the shared protocol and
frozen decisions, do the work, verify, update the ledger, and commit. The prompt
carries **no project content** — that's deliberate (see principle 1). Next
session, point at the next stage file.

*(Ergonomic upgrade: make this a slash command, e.g. `.claude/commands/stage.md`
taking the stage id as an argument, so you type `/stage 3`.)*

---

## 5. Per-stage knobs

Each stage declares a few flags in its header **and** in the DESIGN stage index.
They let each stage choose its own weight, so you don't pay heavy process on
trivial work:

| Flag | Values | Meaning |
|---|---|---|
| `depends` | stage id(s) or `—` | prerequisite stages that must be `done` first |
| `mode` | `direct` \| `brainstorm` | `direct` = state a one-line plan and implement. `brainstorm` = run a design/exploration pass first (e.g. a brainstorming skill), scoped to this stage, treating frozen decisions as settled. |
| `exec` | `inline` \| `subagent(<model>)` | `inline` = implement in this session. `subagent(<model>)` = this session acts as orchestrator and dispatches implementation to a subagent on `<model>`, so the churn (file reads, edits, tool output) stays in the subagent's context, not yours. |
| `model` | e.g. `opus` / `sonnet` / `haiku` | recommended model to run the session (or the subagent) on |
| `effort` | `low`/`med`/`high`/`xhigh` | recommended reasoning effort |

**Choosing the flags (learned guidance):**
- Default to `mode: direct`. Only use `brainstorm` where the stage has **genuine
  open design choices**. Running a full brainstorm on a mechanical one-liner is
  pure ceremony.
- Default to `exec: inline`. Session-per-stage already isolates context, so
  subagents are worth their overhead **only on churn-heavy stages** (lots of
  iteration, config, debugging). Dispatching a subagent to write one line costs
  more than it saves.
- Default to the **cheaper capable model**; reserve the top model for the
  **keystone stage** (the foundation everything depends on) and the **one or two
  design-heavy stages**. Match `effort` to genuine difficulty — most staged work
  is `low`/`med`; reserve `high`/`xhigh` for real reasoning or a thorough design
  pass.

---

## 6. The operating protocol (every stage session)

This lives in `DESIGN.md` and every stage file points at it. The agent, in a
fresh session, must:

1. **Read only what's needed.** The DESIGN *frozen decisions* + the target stage
   file + the ledger (+ any project memory). **Do not scan the whole repo** — that
   defeats the context discipline.
2. **Dependency gate.** If a `depends` stage isn't `done` in the ledger, **stop
   and say so.** Never build on an unbuilt prerequisite.
3. **Honor `mode`.** `direct` → one-line plan, implement. `brainstorm` → design
   pass first, then implement.
4. **Honor `exec`.** `inline` → do it here. `subagent(<model>)` → dispatch
   implementation to a subagent with only the stage file + frozen decisions;
   review its summary and run the acceptance check yourself.
5. **Scope discipline.** Do **only this stage.** If you spot work belonging to
   another stage, **note it in the ledger and leave it untouched** (it may become
   a new stage — see §8).
6. **Finish protocol (required, every session):**
   1. Run the stage's **acceptance check**; **paste the real output.**
   2. Update the stage's **ledger row**: status, absolute date, one-line result,
      verified yes/no, and any **as-built notes** worth keeping (gotchas,
      workarounds, follow-ups, assumptions the next stage should know).
   3. If a decision **changed or was added**, edit the **frozen decisions in
      DESIGN.md — and nowhere else.**
   4. **Commit** (`.plan/` + any artifacts) with a conventional message. **Stop.**

---

## 7. Stage status lifecycle

`todo → doing → done` — plus two important non-linear states:

- **`blocked`** — the stage hit a gate only a human (or another system) can clear,
  e.g. a GUI-only action, a credential, an approval, an external dependency. Write
  what it's blocked on in the ledger and stop; don't fake progress. The scaffold
  handles partial completion gracefully — a `blocked`/`doing` stage is a normal,
  resumable state, not a failure.
- **`skipped`** — decided not to do it; record the one-line reason.

A stage that is human-gated (someone must click something, plug something in) is
best written as a **runbook**: the agent produces exact click-by-click steps + the
verification query, marks the stage `doing/blocked`, and the human completes it.

---

## 8. The design evolves — in one place, and can grow stages

Two things happen on real builds; the method absorbs both **without drift**:

- **Decisions change as reality intrudes.** A threshold turns out wrong, a
  dependency behaves unexpectedly, a security boundary needs tightening. When this
  happens you **amend the frozen decisions in DESIGN.md** (the single source of
  truth) — never patch it into a stage file or carry two versions.
- **New stages are born from shortcuts and discoveries.** If a stage takes a
  shortcut ("deployed manually, skipped the orchestrator"), or you spot follow-up
  work, **add a new stage** to the DESIGN stage index + a ledger row capturing the
  loose ends, rather than silently expanding the current stage's scope. Follow-up
  stages keep each unit small and keep the shortcut visible.

Also track **known gaps and latent hazards explicitly** in the ledger/DESIGN
(things not under version control, footguns, "this script would delete X if run").
Writing them down is what stops them becoming surprises.

---

## 9. File templates (generic)

### `DESIGN.md`

```markdown
# <Project> — design & protocol

Rationale and rejected alternatives live in commit history / project memory.
This file is the executable spec: architecture, frozen decisions, and the
operating protocol every stage session follows.

## Architecture
- <the shape of the target system, in a few bullets>

## Frozen decisions
Change these in THIS file only — never restate them in stage files or prompts.
- <decision>: <value> (+ one-line why if non-obvious)
- <decision>: <value>
- <constraint / boundary / hard rule>

## Stage index & dependencies
| Stage | File | Depends | mode | exec | model | effort |
|---|---|---|---|---|---|---|
| S0 <name> | stage-0-<slug>.md | — | direct | inline | <m> | <e> |
| S1 <name> | stage-1-<slug>.md | S0 | ... | ... | ... | ... |

## Operating protocol (every stage session)
1. Read only: Frozen decisions + the target stage file + LEDGER.md (+ memory).
   Do NOT scan the rest of the repo.
2. Dependency gate: if `depends` isn't `done` in LEDGER.md, stop and say so.
3. Honor `mode` (direct / brainstorm).
4. Honor `exec` (inline / subagent(<model>)).
5. Scope discipline: do only this stage; note stray work in the ledger, leave it.
6. Finish protocol: run acceptance (paste real output) -> update ledger row
   -> amend Frozen decisions here if changed -> commit -> stop.
```

### `LEDGER.md`

```markdown
# Rollout ledger
Status: todo -> doing -> done / blocked / skipped. Update your stage's row at the
end of every session (Operating protocol step 6).

| Stage | Status | Verified | Date | Notes |
|---|---|---|---|---|
| S0 <name> | todo | — | — | <one-line scope / dependency hint> |
| S1 <name> | todo | — | — | needs S0 |
```
*(The Notes cell grows into detailed as-built notes as stages complete — gotchas,
workarounds, follow-ups, and assumptions later stages rely on.)*

### `stage-N-<slug>.md`

```markdown
# S<N> — <title>

**depends:** <S? or —>  **mode:** <direct|brainstorm>  **exec:** <inline|subagent(<model>)>
**model:** <recommended>  **effort:** <low|med|high|xhigh>

> First read `.plan/DESIGN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md`. Follow the Operating protocol, including the finish protocol.

## Goal
<one or two sentences: what this stage delivers>

## Steps
- <small, concrete step>
- <small, concrete step>

## Acceptance
- <a check that produces real, pasteable evidence the stage works>

## Artifacts
<where the outputs land in the repo; note any secrets stay out of git>
```

### `README.md`

```markdown
# `.plan/` — <project> rollout
Ledger-driven, one-stage-at-a-time rollout designed for short, resumable sessions.

## Run a stage
Start a fresh session and paste:
> Follow the instructions in `.plan/stage-<N>-<slug>.md`

## Files
- DESIGN.md  — architecture, frozen decisions, operating protocol (source of truth)
- LEDGER.md  — progress + as-built notes (the only file execution mutates)
- stage-*.md — one small, self-contained stage each

## Context/token discipline
- Session-per-stage keeps context small by default (no subagents needed).
- `exec: subagent(<model>)` stages delegate heavy implementation to a subagent so
  the churn stays out of the orchestrator's context.
```

---

## 10. Two phases of use

### Phase A — Bootstrap a new plan (do this once, at the start)

Give the agent the project idea and this instruction:

> Using the Plan-Driven Staged Rollout method: (1) if the design isn't settled,
> run a design/brainstorming pass with me first; (2) create a dedicated branch;
> (3) scaffold `.plan/` — DESIGN.md (architecture + frozen decisions + stage index
> + operating protocol), LEDGER.md, README.md, and one small `stage-N.md` per
> unit; (4) decompose the work into the **smallest sensible stages** with explicit
> `depends`, and set each stage's `mode`/`exec`/`model`/`effort`; (5) put the hard
> prerequisite (the foundation everything builds on) as S0 and mark every other
> stage as depending on it; (6) commit the scaffold. Don't start implementing
> stages yet.

Decomposition guidance for the agent:
- **Smallest sensible unit per stage.** If a stage has two genuinely different
  mechanisms or a design-heavy part plus mechanical parts, split it.
- **Group by effort, not just by feature.** Several near-identical mechanical
  units can be one stage; a single design-heavy unit deserves its own.
- **Identify the keystone (S0)** — the piece with no prerequisites that everything
  else needs — and gate the rest behind it.
- **Set flags conservatively:** mostly `direct`/`inline`/cheaper-model; escalate
  only where design or churn genuinely warrants it.

### Phase B — Execute stages (repeat, one per session)

Fresh session → paste the runner prompt (§4) → the agent follows the operating
protocol (§6) → it commits and stops. Resume any time by reading the ledger and
running the next `todo` whose `depends` are `done`.

---

## 11. Anti-patterns (things this method exists to prevent)

- **Restating decisions in prompts or stage files.** That creates copies that
  drift. Point at DESIGN; never paste its contents.
- **One giant stage.** Blows context and can't be resumed cleanly. Split it.
- **Brainstorming everything.** Heavy design process on mechanical work is wasted
  tokens. `mode: direct` is the default.
- **Subagents everywhere.** Overhead exceeds benefit on small stages;
  session-per-stage already isolates context. Reserve for churn-heavy stages.
- **Claiming done without evidence.** The acceptance check must actually run and
  its output must land in the ledger.
- **Silent scope creep.** "While I'm here" work on another stage breaks the small-
  unit discipline. Note it, spin a new stage, move on.
- **Editing the design in two places.** Frozen decisions change in DESIGN.md only.
- **Skipping the dependency gate.** Running a stage before its prerequisite is
  built produces plans you can't verify.

---

## 12. Turning this into a skill (your next-session goal)

When you convert this to a skill, the natural shape is:
- **Trigger/description:** "staged, multi-session rollout of a large build with a
  `.plan/` ledger; keep context small, avoid drift, resume freely."
- **Skill body:** §2 (principles), §3 (file layout), §5 (flags), §6 (operating
  protocol), §9 (templates), §11 (anti-patterns).
- **Two entry points**, mirroring §10: a **bootstrap** action (scaffold a new
  `.plan/` from a project description) and a **run-stage** action (execute one
  stage file end-to-end under the operating protocol).
- Consider bundling the **slash command** for the runner prompt and, optionally, a
  tiny script that lists the next runnable stage from the ledger.

Keep the templates in the skill as files to copy, and keep the operating protocol
short enough that it fits comfortably in a stage session's context — its brevity
is part of why the method stays cheap.
