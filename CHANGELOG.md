# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Plugin installs failed on any machine without SSH configured for GitHub, with
  `Host key verification failed`. Both entries used a `github` owner/repo
  source, which Claude Code clones over SSH by default. They now use a `url`
  source with the full `https://` URL, so installs need no SSH key, no
  `known_hosts` entry and no environment variable. Adding the marketplace was
  never affected, which is why this looked like a broken plugin.

### Changed

- `scripts/validate_catalog.py` now rejects `github` sources and any url that
  isn't `https://`, so the SSH-only form can't come back.
- The README now tells users to add the marketplace by its full `https://` URL
  instead of the `by-carlos/claude-plugins` shorthand. Both work — the
  marketplace path falls back to HTTPS when SSH isn't set up — but the shorthand
  is recorded as a GitHub source, so the transport is re-decided by an SSH probe
  on every refresh. The full URL is fetched the same way on every machine.

## [0.2.0] - 2026-08-15

### Added

- `daikenja` plugin entry. Not an assistant — a sage you consult in the shape
  of a Claude Code plugin. It knows your work, the work around you, and where
  to go next. (*) Currently available on private beta.

## [0.1.0] - 2026-07-08

### Added

- `plan-staged-rollout` plugin entry. Claude Code plugin — run big projects as
  many small, resumable sessions instead of one huge one.
