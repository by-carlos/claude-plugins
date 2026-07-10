# Changelog

All notable changes to this marketplace are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the `plan-staged-rollout`
plugin follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
