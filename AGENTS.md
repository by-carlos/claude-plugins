# AGENTS.md — `claude-plugins` (catalog)

**Read [`CLAUDE.md`](CLAUDE.md) — it is the single source of project context and
guardrails for this repository, and it applies to you in full.** Despite the
filename it is not Claude-specific: it covers the distribution model, what
merging here does and does not ship, the git conventions, and the issue-routing
contract for this public repo.

This file exists so that agents and review tools which bootstrap from
`AGENTS.md` find that pointer — notably Copilot code review, which reads
`AGENTS.md` but **not** `CLAUDE.md`. It is deliberately **not** a second copy:
a duplicated ruleset drifts, and three sibling repos in this estate had forked
copies that already had.

## Non-negotiables, restated here so they cannot be missed

These are the rules where *not having read the doc yet* is itself the failure
mode. They are also in `CLAUDE.md`; that copy is authoritative.

- **This repo is the catalog and contains no plugin code.** Its only real
  content is `.claude-plugin/marketplace.json`. Each plugin lives in its own
  repository; this one just points at them.
- **Every plugin entry must use a `url` source over `https://`, pinned to a
  `ref`** — in practice `"ref": "release"`, the branch each plugin repo
  fast-forwards when it releases.
- **Never use a `github` owner/repo source, and never a non-`https://` url.**
  Claude Code clones `github` shorthand sources over SSH by default, so the
  install fails on any machine with no `github.com` host key and no SSH agent —
  every fresh install. Adding the marketplace still works, because that path
  falls back to HTTPS, so the breakage shows up only at install time. CI rejects
  both forms.
- **The README's `marketplace add` line uses the full `https://` URL on
  purpose** — don't shorten it to `by-carlos/claude-plugins`. The shorthand
  works, but it is recorded on the user's machine as a `github` source, so its
  transport is re-decided by an SSH probe on every refresh. CI does not enforce
  this one.
- **Never use a relative-path source** (`"source": "./some-dir"`). It resolves
  against whatever ref the consumer's marketplace clone sits at, which turns
  every merge to `main` here into an immediate release to every user. CI rejects
  it.
- **Merging here does not ship a plugin** — a plugin ships when its own repo
  moves `release`. What merging *does* ship is the catalog itself: adding,
  removing or repointing an entry takes effect on the next
  `/plugin marketplace update`, so **keep `main` correct at all times**.
- **No versions, tags or releases in this repo.** Versioning belongs to each
  plugin's `plugin.json`. Don't reintroduce them here.
- **`CHANGELOG.md` is dated, not versioned** — entries sit under a date heading
  (`## 2026-08-24`), newest first, and there is no `[Unreleased]` section
  because nothing here is ever released. Add an entry for a catalog change
  worth finding later; skip it for wording fixes. CI does not enforce this.
- **Never push directly to `main`, and never merge unilaterally** — propose the
  merge and wait for the maintainer's OK. Squash by default; delete the branch
  after it merges.
- **A source the CI run cannot see reporting as a *skip* is correct, not a
  failure.** `scripts/validate_catalog.py` can only resolve sources the run can
  see. Every catalogued source is public today, so nothing skips and a skip in a
  run means something changed. A source that *is* visible but whose `ref` or
  manifest is missing is a hard error — don't conflate the two.
- **Route issues by subject.** Only catalog-level problems belong here — a
  missing or misdescribed entry, an unresolvable source, a broken install
  command in the README. Anything about a plugin's *behaviour* belongs in that
  plugin's own repo.
- **This repo is public.** An issue body is published the moment it is filed and
  stays indexed even if edited or deleted. Scrub hostnames, LAN IPs, subnets,
  CT/VM names, personal filesystem paths, and raw log pastes; show the rendered
  body and get an explicit OK before filing — every time.

Everything else — and the reasoning behind these — is in
[`CLAUDE.md`](CLAUDE.md).
