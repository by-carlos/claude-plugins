# Build ledger — `plan-staged-rollout` plugin

Statuses: `todo → doing → done`, plus `blocked` / `skipped`. Keep table rows
to ONE line; detail goes in the notes blocks below. Update your stage's row
and notes block at the end of every session (Operating protocol step 7).

## Status

| Stage | Status | Verified | Date | Result |
|---|---|---|---|---|
| S0 Plugin scaffold & manifest | done | yes | 2026-07-08 | plugin.json + skill/commands dirs created, validated |
| S1 Scaffold templates | todo | — | — | — |
| S2 SKILL.md | todo | — | — | — |
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
_(empty)_

### S2 SKILL.md
_(empty)_

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
