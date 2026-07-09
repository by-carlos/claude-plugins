# S0 — Plugin scaffold & manifest

**depends:** —  **mode:** direct  **exec:** inline  **model:** sonnet  **effort:** low

> First read `.plan/PLAN.md` (Frozen decisions + Operating protocol) and
> `.plan/LEDGER.md`. Follow the protocol, including the finish protocol.
> README sections to read: "Status" (planned layout).

## Goal

The plugin's directory skeleton and a valid manifest, so every later stage
has a fixed structure to drop files into.

## Steps

- [ ] Verify the current plugin manifest schema against the official Claude
      Code plugin docs (knowledge may be stale — check required vs optional
      fields before writing).
- [ ] Create `plan-staged-rollout/.claude-plugin/plugin.json` — name
      `plan-staged-rollout`, version `0.1.0`, a one-line description matching
      the README's tagline, author Carlos.
- [ ] Create the empty directories: `plan-staged-rollout/skills/staged-rollout/references/templates/`
      and `plan-staged-rollout/commands/`.

## Acceptance

- `plugin.json` parses (`jq . plan-staged-rollout/.claude-plugin/plugin.json`)
  and contains the fields the docs require.
- The directory tree matches the layout in `PLAN.md` → Architecture.

## Artifacts

`plan-staged-rollout/.claude-plugin/plugin.json` + empty skill/commands dirs.
