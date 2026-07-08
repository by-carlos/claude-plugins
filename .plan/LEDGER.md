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
| S3 `/plan-stages` command | todo | — | — | — |
| S4 `/plan-run` command | todo | — | — | — |
| S5 `/plan-close` command | todo | — | — | — |
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
_(empty)_

### S4 `/plan-run` command
_(empty)_

### S5 `/plan-close` command
_(empty)_

### S6 End-to-end dogfood test
_(empty)_

### SF Plan review
_(empty)_
