# CLAUDE.md — claude-plugins (catalog)

Project instructions for agentic coding in this repository.

This repo is the **`carlos-plugins` marketplace catalog** and contains no plugin
code. Its only real content is `.claude-plugin/marketplace.json`. Each plugin
lives in its own repository; this one just points at them.

## Distribution model

- **Every plugin entry must use a `github` source pinned to a `ref`** — in
  practice `"ref": "release"`, a branch the plugin repo fast-forwards when it
  releases:

  ```json
  {
    "source": "github",
    "repo": "by-carlos/<repo>",
    "ref": "release"
  }
  ```

- **Never use a relative-path source** (`"source": "./some-dir"`). It resolves
  against whatever ref the consumer's marketplace clone sits at, which turns
  every merge to `main` here into an immediate release to every user. CI
  rejects it.
- **Merging here does not ship a plugin.** A plugin ships when its own repo
  moves `release`. What merging here *does* ship is the catalog itself — adding,
  removing or repointing an entry takes effect on the next
  `/plugin marketplace update`, so keep `main` correct at all times.
- **No versions, tags, releases or changelog in this repo.** Versioning belongs
  to each plugin's `plugin.json`. Don't reintroduce them here.

## Git & merge conventions

- **Merge strategy:** **squash merge** by default, unless the maintainer asks
  for another.
- **Branch cleanup:** delete a branch after it merges.
- Merging is never unilateral: propose the merge and wait for the maintainer's
  OK. Never push directly to `main`.

## Capturing follow-up work (GitHub issues)

The generic contract — when to file, the issue body format, labels, and the
Size/Effort discipline — lives in the maintainer's global `CLAUDE.md` /
`AGENTS.md`. This section adds only what is specific to this repo.

- **Tracker & board:** issues live in `by-carlos/claude-plugins` and go to the
  **"Claude Plugins"** project (project 3). Its priority scale is **P0–P4**.
- **Route by subject, not by convenience.** Only catalog-level issues belong
  here — a missing or misdescribed entry, a source that won't resolve, a broken
  install command in the README. Anything about a plugin's *behaviour* belongs
  in that plugin's own repo. If it isn't clear which, ask rather than guess: a
  misfiled issue is one nobody finds again.
- **That board is shared across every Claude plugin repo**, not scoped to this
  one — `by-carlos/plan-staged-rollout` and `by-carlos/daikenja` file there too.
  So don't read the board as a view of this repo: filter by the Repository field
  before concluding anything about what is open here.
- **This repo is public.** An issue body is published the moment it is filed —
  and stays indexed even if edited or deleted afterwards.
- **Scrub before filing.** No hostnames, LAN IPs or subnets, CT/VM/container
  names, personal filesystem paths, email addresses, tokens, or raw log/console
  pastes. Redact to generic placeholders (`<router>`, `<nas>`, `10.x.x.x`,
  `/path/to/repo`) and keep the reproduction abstract enough to stand on its own.
- **Show the rendered body and get an explicit OK before filing — every time.**
  This gate is not waived by a general "capture these" from the maintainer;
  public is a one-way door.

## Validation & secret scanning

- [`scripts/validate_catalog.py`](scripts/validate_catalog.py) runs in CI on
  every push/PR: the manifest parses and is well-formed, no entry uses a
  relative-path source, every `github` source resolves at its pinned ref, and
  README links resolve. Stdlib only. Source resolution only covers repos the
  run can see — a source in a repo the run cannot see reports as a **skip**, not
  a failure, so CI stays honest rather than red. **Every catalogued source is
  public today**, so nothing skips and every entry is genuinely resolved; a skip
  appearing in a run means something changed, not business as usual. A source
  that *is* visible but whose `ref` or manifest is missing is a hard error.
  `GH_TOKEN` resolves private sources locally.
- [gitleaks](https://github.com/gitleaks/gitleaks) runs in CI on every push/PR;
  historical findings would be baselined in `.gitleaks-baseline.json`
  (currently empty). CI-only by design — no local pre-commit hook.
