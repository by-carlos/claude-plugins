# S3 — `/plan-stages` command

**depends:** S1, S2  **mode:** direct  **exec:** inline  **model:** opus  **effort:** med

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md` (incl. S1 + S2 notes). Follow the protocol, including the
> finish protocol. README sections to read: "How it works → 1. Bootstrap",
> "Git model", "Review — the standing final stage".

## Goal

The bootstrap command: from a project idea to a committed `.plan/` scaffold,
with zero stage execution.

## Steps

- [ ] Write `commands/plan-stages.md` with frontmatter (`description`,
      `argument-hint: <project idea>`).
- [ ] Weight gate first: verify the session model is Opus-class or better
      (from the session's own system prompt); state the effort recommendation
      (medium+) as a reminder — never claim to verify effort. On a lighter
      model: warn and offer abort before anything else.
- [ ] Design pass: if the design isn't settled, use
      `superpowers:brainstorming` when available, else the built-in fallback
      (one question at a time, multiple-choice preferred). Outcomes land
      directly as Frozen decisions in the scaffolded `PLAN.md` — never a
      separate spec document.
- [ ] Decomposition: apply the skill's guidance (smallest sensible stages,
      explicit `depends`, keystone S0, conservative flags), then append the
      standing `S-final: plan review` stage.
- [ ] Git strategy question: default branch-per-stage (plan branch +
      `<planbranch>-s<N>` + PR per stage, no per-stage exceptions); offer
      single-plan-branch and trunk as alternatives. Record the choice as a
      frozen decision. Branch creation is proposed to the user, not executed
      unilaterally.
- [ ] Scaffold `.plan/` from `references/templates/`, fill it in, and propose
      the scaffold commit.
- [ ] End announcement: bootstrap is finished, no stage was executed, and the
      user's next action is `/plan-run 0` in a fresh session — stating S0's
      recommended model/effort.

## Acceptance

- `commands/plan-stages.md` exists, frontmatter parses, and a checklist
  review confirms every step above is present in the command flow, in order.
- The command references the skill/templates rather than restating the
  protocol (no second source of truth). Live behavior is verified in S6.

## Artifacts

`plan-staged-rollout/commands/plan-stages.md`
