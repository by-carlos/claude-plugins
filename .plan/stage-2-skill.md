# S2 — SKILL.md

**depends:** S0, S1  **mode:** direct  **exec:** inline  **model:** opus  **effort:** med

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md` (incl. S1 notes). Follow the protocol, including the
> finish protocol. README sections to read: "The idea", "When *not* to use
> this", "Anti-patterns", "Per-stage knobs".

## Goal

The skill body: the method knowledge the commands lean on — when to use it,
how to decompose, how to set flags — kept lean via progressive disclosure to
the templates.

## Steps

- [ ] Write `skills/staged-rollout/SKILL.md` with valid frontmatter: `name:
      staged-rollout`; `description` that triggers on big multi-session
      builds, staged/milestone rollouts, "project too big for one session",
      resumable plans — and explicitly NOT on single-session tasks.
- [ ] Body sections: when to use / when not; the core principles (single
      source of truth, session-per-stage, evidence ledger, verify-before-done);
      decomposition guidance (smallest sensible stage, group by effort,
      keystone S0, standing final review stage); flag heuristics (defaults
      cheap, escalate only for genuine design/churn); git model (default
      branch-per-stage + alternatives, flat branch names, propose-don't-merge);
      review-stage semantics (catalogs, never implements; three outcomes);
      closeout semantics; anti-patterns.
- [ ] Point to `references/templates/` for the file formats instead of
      restating them (progressive disclosure — keep SKILL.md well under the
      size where it stops being cheap to load).
- [ ] Absorb anything still unique in
      `plan-staged-rollout/plan-staged-rollout.prompt.md`, then delete that
      file (per frozen decision; content survives in git history).

## Acceptance

- Frontmatter parses; `name` and `description` present and within Claude
  Code's skill limits.
- Every body section listed above is present; no template content duplicated
  from `references/templates/`.
- `plan-staged-rollout.prompt.md` no longer exists in the repo.

## Artifacts

`plan-staged-rollout/skills/staged-rollout/SKILL.md`; deletion of
`plan-staged-rollout/plan-staged-rollout.prompt.md`.
