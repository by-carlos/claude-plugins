# S5 — `/plan-close` command

**depends:** S2  **mode:** direct  **exec:** inline  **model:** sonnet  **effort:** med

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md` (incl. S2 notes). Follow the protocol, including the
> finish protocol. README sections to read: "How it works → 5. Closeout".

## Goal

The closeout command: verify completion, preserve the story, clean up,
propose the final PR.

## Steps

- [ ] Write `commands/plan-close.md` with frontmatter (`description`, no
      argument).
- [ ] Gate: refuse to run unless every ledger row is `done` or `skipped` —
      list exactly which stages are pending and what to run instead.
- [ ] Distill `PLAN.md` + the ledger (including spin-off candidates and
      accepted-won't-fix items from the review stage) into the final PR body,
      so the why and the as-built story survive on `main`.
- [ ] Delete `.plan/` as the last commit on the plan branch, after offering
      the keep-it option (for projects where the plan doubles as docs).
- [ ] Propose the PR from the plan branch to `main` — user reviews and
      merges; never merge or push unilaterally.
- [ ] End announcement: the plan is closed, PR proposed/opened, nothing left
      to run.

## Acceptance

- `commands/plan-close.md` exists, frontmatter parses, checklist review
  confirms the flow above, including the refusal path. Live behavior
  (refusal with pending stages) verified in S6.

## Artifacts

`plan-staged-rollout/commands/plan-close.md`
