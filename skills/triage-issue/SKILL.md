---
name: triage-issue
description: Triage GitHub issues across one or more repos and rank them into a Projects (v2) board queue — dedup/consolidate, fix hygiene, and set Status/Priority/Size/Effort so `/work-issue next` can burn the queue down. Use for backlog triage, deduplication, or board grooming.
---

Run a reproducible GitHub issue triage session. The output is a **ranked queue on a
GitHub Projects (v2) board** — not a local file — that `/work-issue next` consumes.
Same stages, same format, every run. Skimmable, no filler.

## Board schema (the contract with `/work-issue`)

The board is the source of truth. Triage writes these fields; `/work-issue next`
reads them. Reading and writing project fields needs the `project` scope on `gh`
(`gh auth refresh -s project`).

| Field | Type | Meaning |
|-------|------|---------|
| **Status** | single-select | `Ready` = a Claude Code session can pick it up **now**. Anything not `Ready` (`Backlog`, `In progress`, `In review`, `Done`) is excluded from the queue. |
| **Priority** | single-select `P0`–`P3` | primary sort key |
| **Size** | single-select `XS`–`XL` | secondary sort key (smaller first) |
| **Effort** | single-select | model + reasoning-effort recommendation: `haiku`; `sonnet-{low,med,high,extra,max,ultracode}`; `opus-{low,med,high,extra,max,ultracode}`; or `human` (needs physical/account/GUI access Claude Code can't do) |

**Readiness invariant — set `Status = Ready` only when all hold:**
- Priority, Size, and Effort are all set, **and**
- Effort ≠ `human` (human-only work stays `Backlog` so `next` never grabs it), **and**
- the issue is dispatch-ready (clear repro/constraints/verify — not a stub).

Anything failing these stays `Backlog`. Enable the board's built-in **"Item closed →
Done"** workflow once, so a merged `Closes #n` auto-completes the card — triage never
has to un-queue finished work.

**Queue order** among `Ready` items: `(Priority P0<P1<P2<P3, then Size XS<…<XL, then
issue number asc)`.

<role>
You are running a GitHub issue triage session. Output must be reproducible across runs:
same stages, same format, skimmable, no filler.
</role>

<scope>
- **Repos:** the repos named at invocation (e.g. `by-carlos/linux by-carlos/openwrt`).
  If none are named, default to the current repo.
- **Board:** the Projects v2 board named at invocation (URL or number + owner). If none
  is named, default to the board the in-scope issues already sit on. A single board may
  hold items from several repos — that is expected and fine.
</scope>

<process>
Stage 0 — Gather
- Pull every open issue in scope via `gh`: full body, labels, comments, cross-references
  (`gh issue list`, `gh issue view <n> --comments`).
- Pull the board's items and their fields:
  `gh project item-list <number> --owner <owner> --format json --limit 500`
  (raise `--limit` past the item count — it defaults to 30). Custom fields surface as
  lowercased top-level keys (`status`, `priority`, `size`, `effort`); `content.type`
  distinguishes `Issue` from `PullRequest`; `content.repository` is `owner/repo`.
- Check repo layout only as needed to sanity-check "affected files" claims.
- If `jq` is unavailable, use another parser (e.g. `python -c`) — don't stall on tooling.
- If an issue references images/screenshots you can't render, say so on that issue's line.
  Never guess at unseen content.

Stage 1 — Board & metadata hygiene
- Flag open issues missing from the board.
- Flag `Ready` items that violate the readiness invariant (missing Priority/Size/Effort,
  or Effort = `human`).
- Flag issues with thin or missing labels.
- Flag priority drift: issue body states one priority, board field says another.
Findings only — no writes yet.

Stage 2 — Consolidate & analyze
Output ONE numbered, skimmable list, grouped under these headers, one line per item:
1. **Duplicates** — issues that are the same work; which closes into which survivor.
2. **Consolidate** — distinct issues whose scope overlaps enough that working them
   separately would conflict or re-tread the same files. Merge them into ONE issue:
   name the survivor, rewrite its body to cover the combined scope, bump its Size/Effort
   to match, and close the rest as superseded. Do **not** consolidate loosely-related
   issues — leave those separate; the queue order already places them adjacently.
3. **Gaps** — issues too thin to dispatch (no repro/constraints/verify). Name them;
   these stay `Backlog`, not `Ready`.
4. **Broken/nonsensical** — issues that don't hold up (self-contradictory, reference
   removed code, unfalsifiable). Flag for separate handling — keep them out of the
   dedup/ranking logic.
5. Hygiene items carried from Stage 1.
End Stage 2 with a single go/no-go request covering every proposed write (closures, body
rewrites, consolidations, label/field fixes). Wait for it. Don't ask per-item.

Stage 3 — Apply (only after go-ahead)
- Execute exactly what was approved.
- **Closures/consolidations:** close as duplicate/superseded, comment linking the survivor.
- **Body rewrites:** match the repo's existing issue-body template if one exists;
  otherwise Problem / Proposed fix / Affected files. Apply directly if the repo already
  has template precedent; show the draft first only if it doesn't.
- **Board writes:** set Priority, Size, and Effort on each surviving issue, then flip the
  dispatch-ready ones to `Status = Ready` (honoring the readiness invariant). Use
  `gh project item-edit --id <item-id> --project-id <pid> --field-id <fid> --single-select-option-id <oid>`
  (resolve field/option IDs from `gh project field-list <n> --owner <owner> --format json`).
  Everything not dispatch-ready stays `Backlog`.
- One-line summary of what was applied, no more.

Stage 4 — Rank & report
The board is now the queue. Print ONE markdown table as a **read-only snapshot** of what
you just wrote (it is not the source of truth — the board is), priority first then
smaller-size first:

| # | Issue | Repo | Status | Pri | Size | Effort |

- `Effort` = the value you wrote. For non-`Ready` rows, note why in the Effort cell
  (`human`, `needs refinement`, `broken`).
- No batching / no ⏸ rows — every dispatchable item is a single self-contained issue.
</process>

<output_format>
- Stage 2: numbered list only — no prose paragraphs, no restating issue bodies.
- Stage 4: one table, no restating Stage 2.
- Nothing outside these two structures except the Stage 2→3 go/no-go line and the
  one-line post-apply summary.
</output_format>

<rules>
- Never batch-close, batch-edit, or write board fields without the Stage 2→3 go-ahead.
- Never guess at unreadable content — state the limitation.
- `Ready` is the only readiness signal; there is no separate readiness section.
- Consolidate overlaps into one issue — never leave a "work these together" batch for the
  queue consumer to reconcile.
</rules>
