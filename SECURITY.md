# Security Policy

## Reporting a vulnerability

**Do not open a public issue or pull request for a security problem.** This
repository is public, and an issue body stays indexed even after it is edited or
deleted.

Report privately through GitHub:
[**Report a vulnerability**](https://github.com/by-carlos/claude-plugins/security/advisories/new).
That opens a draft advisory visible only to you and the maintainer.

If that form is unavailable, contact the maintainer,
[Carlos Eng](https://github.com/by-carlos), through his GitHub profile and ask
for a private channel before sending any detail.

Include what you can: the affected marketplace entry, the steps to reproduce,
and what an attacker gains. Scrub the report the same way an issue would be
scrubbed -- placeholders instead of real hostnames, paths, addresses or
credentials.

Expect an acknowledgement within a week. This is a single-maintainer project
worked on in spare time, so a fix may take longer than that; you will be told
where it stands. Please give the maintainer a reasonable window to ship a fix
before disclosing publicly.

## Supported versions

Only the current state of `main` is supported. This repository is a catalog: it
carries the `carlos-plugins` marketplace manifest and nothing else. Claude Code
reads the manifest from `main`, so that is the only state that can affect an
installation; the `v0.2.0` tag is a historical marker, not a distribution
channel.

## What is in scope

This repository holds a marketplace manifest that tells Claude Code where to
fetch plugins from. The risk it carries is *misdirection* -- pointing an
installer at the wrong place. In scope:

- A marketplace entry that resolves to a repository, branch or ref other than
  the one it names.
- A change to the manifest that would cause Claude Code to install a plugin the
  entry does not describe.
- A weakness in this repository's own CI workflows or in the branch protection
  that guards the manifest.
- Secrets or personal data committed to this repository, including in history.

## What is out of scope

- Vulnerabilities inside a listed plugin. Each plugin lives in its own
  repository -- report it there, against that plugin's own security policy.
- Vulnerabilities in Claude Code itself or in the Claude API. Report those to
  their own maintainers.
- The fact that installing a plugin runs its skills and hooks in your session.
  That is the documented purpose, gated on your installing it.
- Anything requiring an attacker who already controls your machine or your
  Claude Code configuration.
