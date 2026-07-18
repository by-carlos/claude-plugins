# triage-issues: rename + incremental gather — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the `triage-issue` skill to `triage-issues` and make its default run incremental — deep-reading only unsettled issues, with a `--full` flag restoring exhaustive behavior.

**Architecture:** This is a prose/skill change (markdown), not code. "Verification" means grep-based reference checks and reading the edited file back, not a test runner. The skill lives at `skills/triage-issue/SKILL.md` and is referenced by `README.md`, `skills/work-issue/SKILL.md`, and `CHANGELOG.md`. Work in git-mv → edit-content → fix-references → changelog order so no step leaves a dangling link.

**Tech Stack:** Markdown skill files, `gh` CLI (documented commands only — nothing runs here), git.

## Global Constraints

- Public identity is "Carlos Eng" / `by-carlos` only — do not introduce other names/handles (verbatim from memory `public-launch-audit`).
- No `plugin.json` / `marketplace.json` change — these are top-level skills, not packaged in the marketplace manifest.
- Changelog is as-you-go under `## [Unreleased]` — never write a dated/versioned heading or bump a version mid-batch (verbatim from `CLAUDE.md` Releasing).
- Do not change the board schema, the readiness invariant, or the `/work-issue` contract.
- Branch `rename-triage-issues` is already checked out and is in-scope for free commits.

---

### Task 1: Rename the skill directory (git-tracked move)

**Files:**
- Move: `skills/triage-issue/SKILL.md` → `skills/triage-issues/SKILL.md`

**Interfaces:**
- Consumes: nothing.
- Produces: new path `skills/triage-issues/SKILL.md` that Tasks 2–5 reference.

- [ ] **Step 1: Move the file with git so history follows**

```bash
git mv skills/triage-issue/SKILL.md skills/triage-issues/SKILL.md
```

- [ ] **Step 2: Verify the old path is gone and the new one exists**

Run:
```bash
test ! -e skills/triage-issue/SKILL.md && test -f skills/triage-issues/SKILL.md && echo OK
```
Expected: `OK`

- [ ] **Step 3: Verify no other files remain in the old directory**

Run: `ls skills/triage-issue 2>/dev/null; echo "exit:$?"`
Expected: `exit:` non-zero (directory removed) — if it lists files, `git mv` them too.

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "refactor(triage-issues): rename skill directory from triage-issue"
```

---

### Task 2: Update the skill's own `name:` frontmatter

**Files:**
- Modify: `skills/triage-issues/SKILL.md:2`

**Interfaces:**
- Consumes: file at new path from Task 1.
- Produces: frontmatter `name: triage-issues` (the invocable slug `/triage-issues`).

- [ ] **Step 1: Edit the frontmatter name**

Change line 2 from:
```
name: triage-issue
```
to:
```
name: triage-issues
```
Leave the `description:` line unchanged for now (Task 4 revises it).

- [ ] **Step 2: Verify**

Run: `grep -n "^name:" skills/triage-issues/SKILL.md`
Expected: `2:name: triage-issues`

- [ ] **Step 3: Commit**

```bash
git add skills/triage-issues/SKILL.md
git commit -m "refactor(triage-issues): update skill name frontmatter"
```

---

### Task 3: Rewrite `<scope>` and Stage 0 for incremental gather

**Files:**
- Modify: `skills/triage-issues/SKILL.md` — the `<scope>` block (~lines 40–46) and `Stage 0 — Gather` (~lines 49–70).

**Interfaces:**
- Consumes: skill body from Task 2.
- Produces: an `<args>` / mode description that Tasks 4 (description) and 6 (rules) rely on; the term "unsettled" defined once here and reused.

- [ ] **Step 1: Add a mode/flags subsection to `<scope>`**

After the existing `- **Board:**` bullet inside `<scope>`, add:

```markdown
- **Mode:** default runs are **incremental** — only *unsettled* issues get the
  expensive per-issue deep read (Stage 0). Passing `--full` at invocation restores
  the exhaustive behavior: every open issue is deep-read and deduped against the
  entire board. Use `--full` when the board may have drifted or a fresh dedup
  against the whole queue is wanted.

An issue is **settled** (skipped in incremental mode) when its board fields already
exclude it from future queue work: `Status = Ready`, **or** `Effort = human`.
Everything else — not on the board, empty Status, empty Effort, `Backlog`,
`In progress`, `In review` — is **unsettled** and gets the full deep read.
```

- [ ] **Step 2: Restructure Stage 0 into a cheap pass and a scoped deep pass**

Replace the first two bullets of `Stage 0 — Gather` (the `Pull every open issue…`
bullet and the `Resolve every cross-reference…` bullet) with:

```markdown
- **Cheap pass (always).** Pull the board's items and their fields first —
  `gh project item-list <number> --owner <owner> --format json --limit 500`
  (raise `--limit` past the item count — it defaults to 30). Custom fields surface as
  lowercased top-level keys (`status`, `priority`, `size`, `effort`); `content.type`
  distinguishes `Issue` from `PullRequest`; `content.repository` is `owner/repo`. Then
  list the open-issue set — `gh issue list` — for numbers, titles, and labels only.
  This is cheap; it always runs in full.
- **Classify.** Using the board fields just pulled, split open issues into **settled**
  (`Status = Ready`, or `Effort = human`) and **unsettled** (everything else). In
  `--full` mode, treat every open issue as unsettled.
- **Deep pass (unsettled only, unless `--full`).** For each unsettled issue, pull the
  full body, comments, and cross-references (`gh issue view <n> --comments`).
  **Resolve every cross-reference, and check whether the work already shipped.** For each
  `#N` an issue names (umbrella, parent, "part of", "supersedes", "duplicate of"), pull
  that issue's state. If it is closed, get *what closed it* —
  `gh issue view <N> --json state,stateReason,closedByPullRequestsReferences` (the closing
  PR lives in `closedByPullRequestsReferences`; it is **not** in `comments`, and an empty
  comments array is not "no explanation"). Then read that PR's body and changed files
  (`gh pr view <p> --json body,files`). A closed-as-`COMPLETED` parent whose PR touches
  the open issue's affected files is a strong signal the fix already merged and the child
  was merely never closed — carry it to Stage 2 §0, do not assume the parent was closed by
  mistake.
- **Settled issues are carried forward on their existing board fields — no deep read,
  no re-examination.** Their Status/Priority/Size/Effort stay as-is.
```

- [ ] **Step 3: Verify the settled/unsettled term and the deep-pass gating are present**

Run:
```bash
grep -c -E "unsettled|Cheap pass|Deep pass" skills/triage-issues/SKILL.md
```
Expected: a count `>= 4`.

- [ ] **Step 4: Read the edited region back and confirm no duplicated cross-reference bullet remains**

Run: `grep -n "Resolve every cross-reference" skills/triage-issues/SKILL.md`
Expected: exactly **one** match (inside the new Deep pass bullet). If two, delete the stale original.

- [ ] **Step 5: Commit**

```bash
git add skills/triage-issues/SKILL.md
git commit -m "feat(triage-issues): incremental gather — deep-read only unsettled issues"
```

---

### Task 4: Wire incremental behavior through Stages 1–2, rules, and the description

**Files:**
- Modify: `skills/triage-issues/SKILL.md` — Stage 1 (~lines 72–80), Stage 2 §1 Duplicates (~line 91), `<rules>` (~lines 138–148), and `description:` (line 3).

**Interfaces:**
- Consumes: "settled/unsettled" term and `--full` flag from Task 3.
- Produces: final skill semantics — no later task depends on these edits.

- [ ] **Step 1: Note that Stage 1 hygiene still covers all items via board fields**

At the top of `Stage 1 — Board & metadata hygiene`, immediately after the
`Stage 1 — Board & metadata hygiene` heading line, insert:

```markdown
Hygiene runs over **all** board items using the fields from the cheap pass — no deep
read needed, so incremental mode never hides a mis-set field. Only the Stage 2
body-level analysis is scoped to unsettled issues.
```

- [ ] **Step 2: Scope the Duplicates dedup and document the `--full` cross-check**

Replace Stage 2 item `1. **Duplicates**` line with:

```markdown
1. **Duplicates** — issues that are the same work; which closes into which survivor.
   In incremental mode, dedup runs **among the unsettled batch only** (those are already
   deep-read, so it is free). Comparing unsettled issues against settled (`Ready` /
   `human`) items happens **only under `--full`**, since that forces deep reads of
   settled items.
```

- [ ] **Step 3: Add a rule pinning the incremental default**

In `<rules>`, after the `- \`Ready\` is the only readiness signal…` bullet, add:

```markdown
- Default runs are incremental: deep-read only unsettled issues (`Status ≠ Ready` **and**
  `Effort ≠ human`). Never deep-read or re-dedup settled issues unless `--full` is passed.
```

- [ ] **Step 4: Update the `description:` frontmatter to say plural + incremental**

Replace line 3 (`description:`) with:

```
description: Triage GitHub issues across one or more repos and rank them into a Projects (v2) board queue — dedup/consolidate, fix hygiene, and set Status/Priority/Size/Effort so `/work-issue next` can burn the queue down. Runs incrementally by default (deep-reads only untriaged issues); pass `--full` for an exhaustive sweep. Use for backlog triage, deduplication, or board grooming.
```

- [ ] **Step 5: Verify all four edits landed**

Run:
```bash
grep -c -E "Hygiene runs over|among the unsettled batch only|Default runs are incremental|Runs incrementally by default" skills/triage-issues/SKILL.md
```
Expected: `4`.

- [ ] **Step 6: Commit**

```bash
git add skills/triage-issues/SKILL.md
git commit -m "feat(triage-issues): thread incremental mode through stages, rules, description"
```

---

### Task 5: Fix all external references to the old name

**Files:**
- Modify: `README.md` (4 occurrences), `skills/work-issue/SKILL.md` (2 occurrences).

**Interfaces:**
- Consumes: new path/slug from Tasks 1–2.
- Produces: a repo with zero references to the old `triage-issue` slug/path (except CHANGELOG history, handled in Task 6).

- [ ] **Step 1: Update `README.md`**

Replace, in order of appearance:
- Heading `### [/triage-issue](skills/triage-issue/SKILL.md)` →
  `### [/triage-issues](skills/triage-issues/SKILL.md)`
- `/triage-issue                                    →  triage the current repo's board` →
  `/triage-issues                                   →  triage the current repo's board`
- `/triage-issue by-carlos/linux by-carlos/openwrt  →  triage several repos onto one board` →
  `/triage-issues by-carlos/linux by-carlos/openwrt →  triage several repos onto one board`
- `pulls the top issue off the \`/triage-issue\` queue and works it.` →
  `pulls the top issue off the \`/triage-issues\` queue and works it.`

(Adjust the arrow alignment so the `→` columns still line up after the extra `s`.)

- [ ] **Step 2: Update `skills/work-issue/SKILL.md`**

Replace both occurrences:
- `board that [\`/triage-issue\`](../triage-issue/SKILL.md) populates)` →
  `board that [\`/triage-issues\`](../triage-issues/SKILL.md) populates)`
- `reads the same board schema \`/triage-issue\` writes` →
  `reads the same board schema \`/triage-issues\` writes`

- [ ] **Step 3: Verify no stale references remain outside CHANGELOG/history**

Run:
```bash
grep -rn "triage-issue\b" README.md skills/work-issue/SKILL.md
```
Expected: **no output** (every hit should now be `triage-issues`). The `\b` keeps
`triage-issues` from matching.

- [ ] **Step 4: Verify the work-issue relative link resolves**

Run: `test -f skills/triage-issues/SKILL.md && echo "link target OK"`
Expected: `link target OK` (confirms `../triage-issues/SKILL.md` from `skills/work-issue/` points at a real file).

- [ ] **Step 5: Commit**

```bash
git add README.md skills/work-issue/SKILL.md
git commit -m "docs(triage-issues): update references to renamed skill"
```

---

### Task 6: Changelog entry

**Files:**
- Modify: `CHANGELOG.md` — add/extend an `## [Unreleased]` section. Do **not** touch
  the two historical `/triage-issue` mentions (lines ~23, ~41) — those record past
  releases and must stay verbatim.

**Interfaces:**
- Consumes: completed rename + feature from Tasks 1–5.
- Produces: nothing downstream.

- [ ] **Step 1: Check whether an `## [Unreleased]` heading already exists**

Run: `grep -n "## \[Unreleased\]" CHANGELOG.md; echo "exit:$?"`
Expected: either a line number (append under it) or `exit:1` (create it above the
newest released section).

- [ ] **Step 2: Add the entry**

If `## [Unreleased]` exists, add these bullets under it. If not, create it directly
below the top-of-file `# Changelog` preamble and above the first `## [x.y.z]` heading:

```markdown
## [Unreleased]

### Changed
- **`/triage-issue` renamed to `/triage-issues`.** Update any saved invocations.
- **Incremental triage by default.** `/triage-issues` now deep-reads only untriaged
  issues (not `Ready`, not `Effort = human`), cutting tokens and wall-time on
  already-groomed boards. Pass `--full` for the previous exhaustive sweep (re-reads
  every issue and dedups against the whole board).
```

- [ ] **Step 3: Verify the two historical mentions are untouched**

Run: `grep -n "triage-issue\b" CHANGELOG.md`
Expected: the same 2 historical lines as before this task (no accidental edits) — the
new bullets use `triage-issues`, so `\b` won't match them.

- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md
git commit -m "docs(triage-issues): changelog for rename + incremental default"
```

---

### Task 7: Final repo-wide reference sweep

**Files:** none (verification only).

**Interfaces:**
- Consumes: all prior tasks.
- Produces: confidence that no dangling reference or old path survives.

- [ ] **Step 1: Confirm the only remaining `triage-issue` (singular, word-boundary) hits are CHANGELOG history**

Run:
```bash
grep -rn "triage-issue\b" --include="*.md" . | grep -v "^./_audit/"
```
Expected: exactly the 2 historical `CHANGELOG.md` lines and nothing else.

- [ ] **Step 2: Confirm the old directory path appears nowhere**

Run: `grep -rn "skills/triage-issue/" --include="*.md" . | grep -v "^./_audit/"`
Expected: **no output**.

- [ ] **Step 3: Confirm the new slug is discoverable**

Run: `grep -rln "triage-issues" --include="*.md" . | grep -v "^./_audit/" | sort`
Expected: at minimum `./CHANGELOG.md`, `./README.md`, `./skills/triage-issues/SKILL.md`, `./skills/work-issue/SKILL.md`, plus the docs/ spec and plan.

- [ ] **Step 4: No commit needed** — verification only. If any check failed, fix in the owning task's file and commit there.
```

