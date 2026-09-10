# claude-plugins

Carlos Eng's [Claude Code](https://code.claude.com/docs/en/overview) plugin
marketplace (`carlos-plugins`).

This repository is a **catalog only** — it holds the marketplace manifest and
nothing else. Each plugin lives in its own repository and is served from that
repository's `release` branch, so a plugin ships when its maintainer moves
`release`, not when something merges here.

## Add the marketplace

From within Claude Code:

```
/plugin marketplace add https://github.com/by-carlos/claude-plugins.git
```

Then install what you want (below). Later, `/plugin marketplace update` pulls
new plugin versions.

Use the full URL rather than the `by-carlos/claude-plugins` shorthand. Both
work, but the shorthand is recorded as a GitHub source, and Claude Code decides
between SSH and HTTPS for those by probing your machine's SSH setup on every
refresh. The full `https://` URL is fetched the same way on every machine and
needs no SSH key.

## Plugins

### [plan-staged-rollout](https://github.com/by-carlos/plan-staged-rollout)

**Run big projects as many small sessions — not one huge one.**

Breaks a large build into *stages*, executes each stage in its own fresh
session, tracks progress in an evidence-based ledger, and keeps every decision
in exactly one place so the plan never drifts. Sessions stay cheap, progress
stays visible, and you can stop and resume whenever you have time.

```
/plugin install plan-staged-rollout@carlos-plugins
```

### [daikenja](https://github.com/by-carlos/daikenja)

**Read, compose, and remember.**

Skills for reading threads and documents, composing messages, and keeping a
per-project markdown ledger of decisions and open items. Claude Code only.

```
/plugin install daikenja@carlos-plugins
```

## Reporting issues

File bugs and feature requests against the **plugin's own repository**, linked
above. Use this repo's tracker only for the catalog itself — a plugin missing
from the manifest, a source that won't resolve, or a broken install command.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Author

Built by **Carlos Eng** —
[GitHub](https://github.com/by-carlos) ·
[LinkedIn](https://www.linkedin.com/in/carlos-eng/)

## License

[FSL-1.1-ALv2](LICENSE) © Carlos Eng — free for any use except building a
competing commercial product, and each release becomes Apache-2.0 two years
after it is made available. Versions released before this change remain MIT.
