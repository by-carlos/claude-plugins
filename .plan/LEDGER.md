# Build ledger — `plan-staged-rollout` plugin

Statuses: `todo → doing → done`, plus `blocked` / `skipped`. Keep table rows
to ONE line; detail goes in the notes blocks below. Update your stage's row
and notes block at the end of every session (Operating protocol step 7).

## Status

| Stage | Status | Verified | Date | Result |
|---|---|---|---|---|
| S0 Plugin scaffold & manifest | done | yes | 2026-07-08 | plugin.json + skill/commands dirs created, validated |
| S1 Scaffold templates | done | yes | 2026-07-08 | Four templates authored; consistency + no-leak checks pass; dependency gate hardened to require merged prerequisite branch |
| S2 SKILL.md | done | yes | 2026-07-08 | SKILL.md authored (lean, points to templates); prompt.md absorbed & deleted |
| S3 `/plan-stages` command | done | yes | 2026-07-08 | plan-stages.md authored as thin wrapper; frontmatter parses, six flow steps in order, references skill/templates |
| S4 `/plan-run` command | done | yes | 2026-07-08 | plan-run.md authored as thin wrapper; frontmatter parses, six ordered flow steps, defers to project PLAN.md with no protocol copy |
| S5 `/plan-close` command | done | yes | 2026-07-08 | plan-close.md authored as thin wrapper; frontmatter parses, six ordered flow steps including refusal gate, distillation, and cleanup-with-keep-option |
| S6 End-to-end dogfood test | todo | — | — | — |
| SF Plan review | todo | — | — | — |

## Notes

As-built notes, acceptance evidence, gotchas, handoff notes. One block per
stage; sessions read only the blocks of their `depends` stages.

### S0 Plugin scaffold & manifest
Verified plugin.json schema against current Claude Code docs
(`code.claude.com/docs/en/plugins-reference`): only `name` is required;
used `name`, `version`, `description`, `author` (all recognized metadata
fields).

Created:
- `plan-staged-rollout/.claude-plugin/plugin.json`
- `plan-staged-rollout/skills/staged-rollout/references/templates/` (empty, `.gitkeep`)
- `plan-staged-rollout/commands/` (empty, `.gitkeep`)

Acceptance evidence:
```
$ python -c "import json; json.load(open('plan-staged-rollout/.claude-plugin/plugin.json', encoding='utf-8'))"
# parses cleanly, no exception
$ find plan-staged-rollout -type f | sort
plan-staged-rollout/.claude-plugin/plugin.json
plan-staged-rollout/README.md
plan-staged-rollout/commands/.gitkeep
plan-staged-rollout/plan-staged-rollout.prompt.md
plan-staged-rollout/skills/staged-rollout/references/templates/.gitkeep
```
Tree matches PLAN.md → Architecture (skills/commands dirs empty pending S1-S4).
No `jq` available in this shell; validated with Python's `json` module instead.

### S1 Scaffold templates
Authored the four scaffold templates `/plan-stages` copies:
`plan-staged-rollout/skills/staged-rollout/references/templates/{PLAN,LEDGER,stage-N,README}.md`.
They carry the frozen decisions' flag set (`depends/mode/exec/model/effort`),
the ledger split (one-line status table + per-stage notes blocks), checkbox
Steps, evidence-based Acceptance, and the full operating protocol. Placeholders
use a single `<angle-bracket>` style throughout. Removed the now-redundant
`templates/.gitkeep` (S0 left it; the dir now has real content).

Cross-checked against the pilot (`C:\GitHub\linux\.plan`, read-only): templates
cover blocked/runbook stages, follow-up stages, and frozen-decision amendments
(LEDGER notes state-guide comment + PLAN finish-step 3), while fixing the
pilot's known flaw — the pilot crammed ~500-word notes into ledger table cells;
these templates force one-line rows with detail in notes blocks. No pilot
homelab/logging content leaked in.

**Frozen-decision amendment (Operating protocol step 3 + 4):** the dependency
gate now requires each `depends` stage to be BOTH `done` in the ledger AND its
branch/PR merged into the plan branch (with a `git fetch` first), and step 4
fast-forwards the plan branch before branching. This came directly from a real
miss this session: S1 was first branched off the plan branch *before* S0's PR
was merged, so it silently lacked S0's work. Hardened in both this file's
protocol and the deliverable template `PLAN.md`.

Acceptance evidence:
```
$ ls -1   # dir holds exactly the four templates
LEDGER.md
PLAN.md
README.md
stage-N.md
$ grep "Stage | Status | Verified | Date | Result" LEDGER.md   # ledger cols
15:| Stage | Status | Verified | Date | Result |
$ grep "Stage | File | Depends | mode | exec | model | effort" PLAN.md  # index cols
39:| Stage | File | Depends | mode | exec | model | effort |
$ grep -rhoE "\b(todo|doing|done|blocked|skipped)\b" . | sort -u   # status vocab
blocked doing done skipped todo   # no stray statuses
$ grep -rniE "victorialogs|ofelia|homelab|syslog|mobydock|komodo|rsyslog|\bvector\b|haos|adguard|synology|proxmox|deadman|logsql" .
clean   # no pilot leakage
$ grep -rnoE "\{[a-z_]+\}|FIXME|XXX|TODO_" .
angle-brackets only   # single placeholder style
```
All Acceptance criteria met: four templates exist, one consistent placeholder
style, internal consistency (statuses / table columns / file names / flag names
identical and matching frozen decisions), no pilot-specific content.

### S2 SKILL.md
Wrote `plan-staged-rollout/skills/staged-rollout/SKILL.md` — the method body the
commands lean on. Sections: when to use / when not; core principles (single
source of truth, session-per-stage, evidence ledger, verify-before-done);
decomposition guidance (smallest sensible stage, group by effort, keystone S0,
standing final review stage); statuses + human-gated `blocked` runbook pattern;
flag heuristics (defaults cheap, escalate only for genuine design/churn); git
model (branch-per-stage default + alternatives, flat names, propose-don't-merge);
review-stage semantics (catalogs, three outcomes, never implements); closeout
semantics; anti-patterns. Formats are delegated to `references/templates/` via
progressive disclosure — no template content restated (PLAN/LEDGER/stage-N/README
formats are pointed at, not duplicated).

Absorbed `plan-staged-rollout/plan-staged-rollout.prompt.md` (old solution-agnostic
method doc) into SKILL.md + the S1 templates + README, then deleted it per the
frozen decision (content survives in git history). The one nugget not already
elsewhere in the *skill* — the `blocked`-stage runbook pattern and explicit
gap/hazard tracking — was pulled into the new "Statuses and human-gated stages"
section.

Acceptance evidence:
```
$ python -c "... parse frontmatter, check field lengths ..."
name: 'staged-rollout' len 14
desc len: 577
OK frontmatter parses; name & description present and within limits
  # name == 'staged-rollout' (<=64); description 577 chars (<=1024 Claude Code limit)

$ grep -nE '^## ' SKILL.md   # every required body section present
19:## When to use it
26:## When NOT to use it
41:## Core principles
60:## Decomposing the work
71:## Flag heuristics
89:## Statuses and human-gated stages
108:## Git model
135:## The final review stage
154:## Closeout
164:## Anti-patterns this exists to prevent

$ test -f plan-staged-rollout/plan-staged-rollout.prompt.md && echo EXISTS || echo absent
deleted: confirmed absent
```
Description triggers on big multi-session/staged/milestone rollouts and
resumable plans, and explicitly excludes single-session/≤3-session work.

### S3 `/plan-stages` command
Wrote `plan-staged-rollout/commands/plan-stages.md` — the bootstrap wrapper. It
loads the `staged-rollout` skill for method, points at
`${CLAUDE_PLUGIN_ROOT}/skills/staged-rollout/references/templates/` for the file
formats, and drives six ordered flow steps: (1) weight gate first — Opus-class
model verified from the session, effort medium+ as a reminder, warn+offer-abort
on a lighter model before any work; (2) design pass only if unsettled —
`superpowers:brainstorming` when installed else a one-question-at-a-time
multiple-choice fallback, outcomes landing as Frozen decisions in the scaffolded
`PLAN.md`, never a separate spec; (3) decompose per skill guidance (smallest
stages, explicit `depends`, keystone S0, cheap flags) then append the standing
`SF: plan review` stage; (4) git-strategy question (default branch-per-stage;
single-plan-branch and trunk offered; recorded as a frozen decision; no branch
created at bootstrap); (5) scaffold from templates, fill placeholders, propose
the scaffold commit; (6) end announcement — bootstrap finished, no stage
executed, next action `/plan-run 0` in a fresh session with S0's model/effort.
No protocol restated — the file explicitly names the skill+templates as the
single source of truth and tells the flow to reference, not duplicate, it.

Acceptance evidence:
```
$ python -c "... parse frontmatter, assert description + argument-hint present"
frontmatter OK
  description: Bootstrap a staged-rollout .plan/ from a project i ...
  argument-hint: <project idea>

$ grep -nE '^[0-9]+\. \*\*' plan-stages.md   # six flow steps, in order
24:1. **Weight gate (first, before anything else).**
32:2. **Design pass (only if the design isn't already settled).**
41:3. **Decompose.**
47:4. **Git strategy question.**
55:5. **Scaffold and commit.**
62:6. **End announcement.**

$ grep -nE 'staged-rollout|references/templates|single source of truth' plan-stages.md
10:wrapper around the `staged-rollout` skill; the skill and its
11:`references/templates/` are the single source of truth for the method and file
16:First, load the method: invoke the **`staged-rollout`** skill ...
```
Checklist review: every plan step is present and in order — frontmatter
(`description` + `argument-hint: <project idea>`), weight gate first, design
pass with brainstorming/fallback → frozen decisions, decomposition + appended
`SF`, git-strategy question with alternatives recorded as a frozen decision and
no unilateral branch creation, scaffold-from-templates + proposed commit, and
the end announcement pointing at `/plan-run 0`. The command references the
skill/templates rather than restating the protocol (no second source of truth).
Live behavior is deferred to S6 (dogfood).

### S4 `/plan-run` command
Wrote `plan-staged-rollout/commands/plan-run.md` — the stage runner. It is a
thin ergonomic wrapper: it does NOT carry the operating protocol. Instead it
(1) locates `.plan/` and resolves `$ARGUMENTS` to `stage-<N>-<slug>.md`, erroring
clearly if `.plan/` is absent (points to `/plan-stages`) or the number matches no
stage file (lists the valid ones); (2) reads and defers to the project's own
`.plan/PLAN.md` Operating protocol verbatim (read-scope, dependency gate,
mode/exec, scope discipline, finish protocol all come from there — so a `.plan/`
keeps working standalone via "Follow the instructions in `.plan/stage-N-...md`");
(3) weight check — model verified from the system prompt, effort reminded not
verified, warn+offer continue/abort when the session is lighter than the stage's
flags; (4) surfaces the protocol's dependency gate; (5) resume support — if the
ledger row is `doing`, continue from unticked checkboxes + handoff note (and
confirm before redoing a `done` stage); (6) end announcement — outcome
(`finished`/`blocked`/`doing` with what's pending), the next runnable stage as an
exact `/plan-run <N>` command with its recommended model/effort, or `/plan-close`
when none remain.

Acceptance evidence:
```
$ python -c "... parse frontmatter, assert description + argument-hint present"
OK frontmatter parses
  description len: 161
  argument-hint: <stage number>

$ grep -nE '^[0-9]+\. \*\*' plan-run.md   # six flow steps, in order
18:1. **Locate `.plan/`.**
24:2. **Defer to the project protocol.**
30:3. **Weight check (ergonomic add).**
38:4. **Dependency gate (ergonomic surfacing of the protocol's rule).**
43:5. **Resume support.**
49:6. **End announcement.**

$ grep -niE 'read only:|weight check:|dependency gate:|finish protocol|scope discipline:|honor .mode' plan-run.md
26:   `mode`/`exec` handling, scope discipline, and the finish protocol all come
   # single hit is an explicit DEFERRAL ("...come from that file, not from this
   # command"), not a copy of the protocol steps — grep-level no-copy check passes.
```
Grep-level check confirms the command contains no copy of the operating protocol
steps; it references/defers to the project's `PLAN.md`. Live behavior deferred to
S6 (dogfood).

### S5 `/plan-close` command
Wrote `plan-staged-rollout/commands/plan-close.md` — the closeout wrapper. No
argument (matches the frozen decision). Six ordered steps: (1) locate `.plan/`,
refusing gracefully if absent; (2) completion gate — refuses to run unless
every `LEDGER.md` row is `done` or `skipped` (including stages the `SF` review
spawned), listing exactly which stages are pending and what to run instead
(`/plan-run <N>` or resolve the `blocked` runbook), stopping before any
distillation/cleanup; (3) distill `PLAN.md` + the full ledger — including the
`SF` stage's spin-off candidates and accepted-won't-fix items — into a
summarized (not pasted-raw) final PR body, so the why and as-built story
survive on `main`; (4) clean up `.plan/` — offers delete-as-last-commit
(default) vs keep-for-docs, proposes the delete commit and waits for the user;
(5) proposes the final PR from the plan branch to `main`, never merges/pushes
unilaterally; (6) end announcement — plan closed, PR proposed/opened, nothing
left to run.

Acceptance evidence:
```
$ python -c "... parse frontmatter, assert description present, no argument-hint ..."
description: Close out a finished staged-rollout .plan/ — verify completion,
  distill the story into a final PR body, clean up .plan/, and propose the PR
  to main.
OK: frontmatter parses, description present, no argument-hint

$ grep -nE '^[0-9]+\. \*\*' plan-close.md   # six flow steps, in order
15:1. **Locate `.plan/`.**
19:2. **Completion gate.**
26:3. **Distill the story.**
38:4. **Clean up `.plan/`.**
46:5. **Propose the final PR.**
50:6. **End announcement.**
```
Checklist review confirms the refusal path (lists pending stages + what to run
instead), the distillation step folding in spin-off/won't-fix items from the
review stage, the delete-with-keep-option cleanup, and the propose-never-merge
PR step. Live behavior (refusal with pending stages) is deferred to S6
(dogfood), per the stage file's Acceptance note.

### S6 End-to-end dogfood test
_(empty)_

### SF Plan review
_(empty)_
