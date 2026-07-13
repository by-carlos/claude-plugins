# claude-plugins

Carlos Eng's [Claude Code](https://code.claude.com/docs/en/overview) plugin
marketplace (`carlos-plugins`).

## Plugins

### [plan-staged-rollout](plan-staged-rollout/README.md)

**Run big projects as many small sessions — not one huge one.**

Breaks a large build into *stages*, executes each stage in its own fresh
session, tracks progress in an evidence-based ledger, and keeps every decision
in exactly one place so the plan never drifts. Sessions stay cheap, progress
stays visible, and you can stop and resume whenever you have time.

```
/plan-stages <idea>  →  design + decompose into .plan/ (once)
/plan-run 3          →  execute one stage in a fresh, cheap session (repeat)
/plan-close          →  final PR, cleanup, done
```

See the [plugin README](plan-staged-rollout/README.md) for the full method,
the git model, and when *not* to use it.

## Install

From within Claude Code:

```
/plugin marketplace add by-carlos/claude-plugins
/plugin install plan-staged-rollout@carlos-plugins
```

Installed plugin commands are namespaced, e.g.
`/plan-staged-rollout:plan-stages`.

## Bonus: standalone commands

The [`commands/`](commands/) directory holds standalone slash commands that
aren't part of any plugin — install one by copying it into
`~/.claude/commands/`.

### [/work-issue](commands/work-issue.md)

**Work a GitHub issue end-to-end** — read the full thread, sanity-check the
scope (pushes back on epics and one-liners), branch as
`<type>/<issue>-<slug>`, implement with conventional commits, open a PR that
closes the issue, and squash-merge only after explicit confirmation.

```
/work-issue 42          →  work issue #42, based on main
/work-issue 42 develop  →  same, based on develop
```

## Author

Built by **Carlos Eng** —
[GitHub](https://github.com/by-carlos) ·
[LinkedIn](https://www.linkedin.com/in/carlos-eng/)

## License

[MIT](LICENSE) © Carlos Eng
