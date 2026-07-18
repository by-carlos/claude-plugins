# Design — `triage-issues`: rename + incremental gather

**Date:** 2026-07-18
**Skill:** `skills/triage-issue/` → `skills/triage-issues/`

## Problem

`triage-issue` re-reads the entire open-issue backlog on every run — full bodies,
`--comments`, cross-reference resolution, and closing-PR diffs for each issue. On a
mostly-triaged board this re-does expensive Tier-2 reads for issues that are already
settled, wasting wall-time and tokens that scale with *total* issues instead of *new*
ones.

## Goals

1. Rename the skill to `triage-issues` (plural).
2. Make the default run **incremental**: deep-read only unsettled issues.
3. Provide a `--full` escape hatch that restores the old exhaustive behavior.

## 1. Rename

- Directory: `skills/triage-issue/` → `skills/triage-issues/`.
- Frontmatter `name: triage-issue` → `triage-issues`.
- Update references: `README.md` (4 occurrences), `skills/work-issue/SKILL.md`
  (2 occurrences, including the relative link `../triage-issue/SKILL.md`).
- Add a `CHANGELOG.md` entry under `## [Unreleased]` noting the rename and the
  incremental default. No `plugin.json` / `marketplace.json` change — these are
  top-level skills, not packaged in the marketplace manifest.

## 2. Incremental gather (default)

Split Stage 0 into two passes.

**Cheap pass (always):**
- `gh project item-list <n> --owner <owner> --format json --limit 500` — one call,
  yields `status` and `effort` per board item.
- `gh issue list` for the open-issue set (numbers, titles, labels) — no bodies.

**Deep pass (scoped):** the expensive Tier-2 reads — `gh issue view --comments`,
cross-reference resolution, `closedByPullRequestsReferences`, closing-PR diffs — run
**only for unsettled issues**.

**Settled** = an issue whose board fields already exclude it from future queue work:
- `Status = Ready`, **or**
- `Effort = human`.

Settled issues are carried forward using their existing board fields, with **no deep
read** and **no re-examination** (per decision: skip `human` entirely).

**Unsettled** = everything else: not on the board, empty Status, empty Effort,
`Backlog`, `In progress`, `In review`, etc. These get the full Tier-2 treatment.

## 3. Dedup split

- **New-vs-new** (dedup *among* the unsettled batch): **always on**. These issues are
  already deep-read, so comparing them costs nothing.
- **New-vs-settled** (does an unsettled issue duplicate a `Ready`/`human` item?): runs
  **only under `--full`**, because it forces deep reads of settled items.

## 4. The `--full` flag

One blunt "do it properly" mode:
- Deep-reads **every** open issue regardless of Status/Effort (old behavior).
- Dedups the unsettled batch against the **entire** board, including `Ready` and
  `human` items.

Documented as the recovery path: use it when the board may have drifted, or when a
fresh dedup against the whole queue is wanted.

## 5. Correctness guardrails

Incremental mode must not let a mis-set board field hide forever:

- **Stage 1 hygiene runs over all items using board fields already in hand** from the
  cheap pass — no extra tokens. So a `Ready` item violating the readiness invariant
  (missing Priority/Size/Effort, or `Effort = human`) is still flagged without a deep
  read, as is priority drift. Only the *body-level* deep analysis is skipped for
  settled items.

## Non-goals

- No change to the board schema, the readiness invariant, or the `/work-issue`
  contract.
- No change to Stage 3 apply logic or Stage 4 reporting beyond reflecting which
  issues were examined.
