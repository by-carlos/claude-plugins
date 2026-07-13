# Changelog

All notable changes to this marketplace are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the `plan-staged-rollout`
plugin follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **`plan-staged-rollout`:** `/plan-stages` bootstrap now computes the modal `model`
  across the stage index and, when a strict majority of stages share one, recommends
  setting it as the session default (and notes it in the scaffolded `.plan/README.md`)
  so the per-stage weight gate only prompts on the exceptions. Bootstrap-time
  convenience only — the stage index stays the authoritative, individually-checked
  home for each stage's `model`/`effort` (#18).
- **`plan-staged-rollout`:** a `.plan/`-aware `SessionStart` hook — opening a fresh
  session in a repo with an active staged rollout now automatically surfaces the
  rollout and its next runnable stage (a `doing` stage to resume, else the first
  `todo` whose `depends` are all `done`), with the stage's recommended model/effort
  and the exact `/plan-run` invocation. It offers, never auto-runs — the weight
  check and dependency gate in `PLAN.md` still govern execution. No `.plan/` in the
  repo → the hook emits nothing; malformed files or parse ambiguity fail silent
  (#13). Cross-platform via the polyglot `run-hook.cmd` wrapper (Windows cmd.exe +
  Unix), mirroring Superpowers' hook layout.

### Fixed

- **`plan-staged-rollout`:** stage sessions and closeout now run a **Preflight & sync**
  block (defined once in the template `PLAN.md`'s operating protocol) before trusting
  the ledger — fetch, fast-forward the plan branch, clean-tree and HEAD-position
  checks, and a ledger-vs-reality reconcile that reports and stops on drift instead of
  auto-repairing (#4; instances #3, #6, #16, #17, #19).
- **`plan-staged-rollout`:** `/plan-run` and `/plan-close` locate the plan via
  `plan-*` branches when `.plan/` is not in the working tree, instead of advising a
  second bootstrap (#3); `/plan-close`'s completion gate also fails on open or
  unmerged stage PRs (#6).
- **`plan-staged-rollout`:** stage PRs pin their base to the plan branch
  (`gh pr create --base plan-<slug>`) (#17); the ledger `done` edit moves to the plan
  branch after the stage PR merges (#19); redo of a `done` stage cuts a fresh
  `-redo-<K>` branch from the plan branch tip.
- **`plan-staged-rollout`:** the `PLAN.md` stage index is now the single authoritative
  home for each stage's `depends` / `mode` / `exec` / `model` / `effort`; stage files
  no longer restate them, ending the two-copies-that-drift ambiguity. Adding a
  PLAN.md stage index row is now a required part of a review-spawned stage's outcome,
  so `/plan-run`'s weight check and next-runnable logic can see it (#5).

## [0.1.0] — 2026-07-10

Initial public release of the `carlos-plugins` marketplace.

### Added

- **`plan-staged-rollout` plugin (0.1.0)** — run big builds as many small, resumable
  sessions instead of one huge one. Decomposes a project into dependency-ordered
  `.plan/` stages with an evidence ledger, then executes one stage per fresh session.
  - Commands: `/plan-stages` (design + decompose an idea), `/plan-run` (execute one
    stage), `/plan-close` (final PR and cleanup).
  - Bundled `staged-rollout` skill documenting the method, the git model, and when
    *not* to use it.
- Marketplace manifest, root and plugin READMEs, and MIT license.

[0.1.0]: https://github.com/by-carlos/claude-plugins/releases/tag/v0.1.0
