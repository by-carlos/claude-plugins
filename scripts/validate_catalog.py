#!/usr/bin/env python3
"""Validate the marketplace catalog: the manifest parses and is well-formed,
every plugin source is an https:// git URL that actually resolves at its pinned
ref, and README links resolve. Stdlib only.

Plugin sources must be `url` sources over https://. A `github` owner/repo
source is rejected: Claude Code clones those over SSH by default, which fails
on any machine that has no github.com entry in known_hosts and no key loaded —
a fresh install, in other words. Relative-path sources are rejected too; they
resolve against whatever ref the consumer's marketplace clone sits at, which
would make every merge to main an immediate release.

Source resolution needs network access and only works for repositories this
run can actually see. A source that isn't publicly visible — a private plugin
repo, or an unauthenticated run — is reported as a skip rather than a failure;
a source that *is* visible but whose ref or manifest is missing is a hard
error. Set GH_TOKEN (or GITHUB_TOKEN) to resolve private sources too."""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".claude-plugin" / "marketplace.json"
API = "https://api.github.com"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TIMEOUT = 15
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

errors = []
skipped = []


def err(msg):
    errors.append(msg)


def api_get(path, raw=False):
    """GET a GitHub API path. Returns (status, body); status None means the
    request never completed (offline, DNS failure, timeout)."""
    request = urllib.request.Request(f"{API}{path}")
    request.add_header(
        "Accept", "application/vnd.github.raw" if raw else "application/vnd.github+json"
    )
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.status, response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except (urllib.error.URLError, TimeoutError):
        return None, ""


def load_manifest():
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err(f"marketplace.json: invalid JSON ({e})")
    except FileNotFoundError:
        err("marketplace.json: file not found")
    return None


def check_source(name, source):
    """A published plugin must be sourced over https:// from another repo at a
    pinned ref."""
    if isinstance(source, str):
        err(
            f"marketplace.json: plugin '{name}' uses a relative-path source "
            f"('{source}'); published plugins must use an https:// url source"
        )
        return
    if not isinstance(source, dict):
        err(f"marketplace.json: plugin '{name}' has a malformed 'source'")
        return
    kind = source.get("source")
    if kind == "github":
        err(
            f"marketplace.json: plugin '{name}' uses a 'github' owner/repo "
            f"source; Claude Code clones those over SSH by default, which "
            f"fails on a machine with no github.com host key or SSH agent. "
            f"Use {{\"source\": \"url\", \"url\": \"https://github.com/"
            f"{source.get('repo', '<owner>/<repo>')}.git\", \"ref\": ...}}"
        )
        return
    if kind != "url":
        err(f"marketplace.json: plugin '{name}' has unsupported source type '{kind}'")
        return
    url, ref = source.get("url"), source.get("ref")
    if not url or not ref:
        err(f"marketplace.json: plugin '{name}' source is missing 'url' or 'ref'")
        return
    if not url.startswith("https://"):
        err(
            f"marketplace.json: plugin '{name}' source url '{url}' is not "
            f"https://; SSH and shorthand URLs fail on machines without SSH "
            f"configured for the host"
        )
        return
    repo = github_repo(url)
    if repo is None:
        skipped.append(f"{name} ({url}@{ref}): not a github.com URL, cannot resolve")
        return
    resolve(name, repo, ref)


def github_repo(url):
    """owner/repo for a github.com https URL, else None."""
    match = re.fullmatch(
        r"https://github\.com/([A-Za-z0-9._-]+/[A-Za-z0-9._-]+?)(?:\.git)?/?", url
    )
    return match.group(1) if match else None


def resolve(name, repo, ref):
    status, _ = api_get(f"/repos/{repo}")
    if status is None:
        skipped.append(f"{name} ({repo}@{ref}): network unavailable")
        return
    if status == 404:
        skipped.append(
            f"{name} ({repo}@{ref}): repository not visible to this run "
            f"(private, or no token)"
        )
        return
    if status != 200:
        skipped.append(f"{name} ({repo}@{ref}): GitHub API returned HTTP {status}")
        return

    status, body = api_get(
        f"/repos/{repo}/contents/.claude-plugin/plugin.json?ref={ref}", raw=True
    )
    if status is None:
        skipped.append(f"{name} ({repo}@{ref}): network unavailable")
        return
    if status == 404:
        err(
            f"marketplace.json: plugin '{name}' does not resolve — "
            f"{repo}@{ref} has no .claude-plugin/plugin.json (ref missing or "
            f"plugin not at the repo root)"
        )
        return
    if status != 200:
        skipped.append(f"{name} ({repo}@{ref}): GitHub API returned HTTP {status}")
        return
    try:
        manifest = json.loads(body)
    except json.JSONDecodeError as e:
        err(f"marketplace.json: plugin '{name}' — plugin.json at {repo}@{ref} is invalid JSON ({e})")
        return
    if manifest.get("name") != name:
        err(
            f"marketplace.json: plugin '{name}' — plugin.json at {repo}@{ref} "
            f"declares name '{manifest.get('name')}'"
        )
    if not manifest.get("version"):
        err(f"marketplace.json: plugin '{name}' — plugin.json at {repo}@{ref} has no version")


def validate_manifest():
    manifest = load_manifest()
    if manifest is None:
        return
    for key in ("name", "owner"):
        if not manifest.get(key):
            err(f"marketplace.json: missing or empty '{key}'")
    plugins = manifest.get("plugins")
    if not plugins:
        err("marketplace.json: 'plugins' is missing or empty")
        return
    seen = set()
    for entry in plugins:
        name = entry.get("name")
        if not name:
            err("marketplace.json: a plugin entry has no 'name'")
            continue
        if name in seen:
            err(f"marketplace.json: duplicate plugin entry '{name}'")
        seen.add(name)
        if not entry.get("description"):
            err(f"marketplace.json: plugin '{name}' has no 'description'")
        if "source" not in entry:
            err(f"marketplace.json: plugin '{name}' has no 'source'")
            continue
        check_source(name, entry["source"])


def validate_readme_links():
    for readme in sorted(ROOT.rglob("README.md")):
        if ".git" in readme.relative_to(ROOT).parts:
            continue
        text = readme.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            if not (readme.parent / target_path).resolve().exists():
                err(f"{readme.relative_to(ROOT)}: broken link to '{target}'")


def main():
    validate_manifest()
    validate_readme_links()

    for note in skipped:
        print(f"validate-catalog: SKIPPED source check for {note}")

    if errors:
        print(f"validate-catalog: {len(errors)} error(s):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("validate-catalog: OK")


if __name__ == "__main__":
    main()
