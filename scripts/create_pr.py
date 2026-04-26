#!/usr/bin/env python3
"""Creates a git branch, commits wiki changes, and opens a GitHub PR."""

import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

LOG_FILE = Path("tmp/validation-log.json")


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        if check:
            sys.exit(result.returncode)
    return result


def has_changes() -> bool:
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    return bool(result.stdout.strip())


def main() -> None:
    if not has_changes():
        print("No git changes detected. Skipping PR creation.")
        sys.exit(0)

    today = date.today().isoformat()
    branch = f"wiki-gaps-{today}"

    run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"])
    run(["git", "config", "user.name", "Wiki Gap Bot"])
    run(["git", "checkout", "-b", branch])
    run(["git", "add", "content/"])
    run(["git", "commit", "-m", f"wiki: Automatische Lückenfüllung {today}"])
    run(["git", "push", "origin", branch])

    # Build PR body from validation log
    topics: list[dict] = []
    if LOG_FILE.exists():
        for entry in json.loads(LOG_FILE.read_text(encoding="utf-8")):
            if entry.get("status") == "applied":
                topics.append(entry)

    body_lines = [
        "## Wiki-Gap-Filling – automatischer PR",
        "",
        f"Erstellt: {today}",
        "",
        "### Erweiterte Seiten",
        "",
    ]
    if topics:
        for t in topics:
            conf = t.get("confidence", "?")
            body_lines.append(f"- **{t['topic']}** → `{t['target']}` (Konfidenz: {conf})")
            for w in t.get("warnings", []):
                body_lines.append(f"  - ⚠️ {w}")
    else:
        body_lines.append("_Keine Seiten direkt geändert (nur wiki-gaps.md aktualisiert)._")

    body_lines += [
        "",
        "---",
        "",
        "## Review-Checkliste",
        "",
        "- [ ] Quellen geprüft und erreichbar",
        "- [ ] Kein Duplikat zu bestehender Seite",
        "- [ ] Wikilinks sinnvoll und korrekt verlinkt",
        "- [ ] Inhalt sachlich korrekt",
        "- [ ] Keine Marketing- oder KI-Formulierungen",
        "- [ ] Markdown-Struktur intakt",
        "- [ ] Bestehender Inhalt vollständig erhalten",
        "",
        "_Nach Merge: `status: review` in `content/wiki-gaps.md` manuell auf `- [x]` setzen._",
    ]

    result = run(
        [
            "gh", "pr", "create",
            "--title", f"Wiki Lückenfüllung – {today}",
            "--body", "\n".join(body_lines),
            "--base", "main",
            "--head", branch,
        ],
        check=False,
    )

    if result.returncode != 0:
        print("PR creation failed. Branch was pushed; create the PR manually.", file=sys.stderr)
        sys.exit(1)

    pr_url = result.stdout.strip()
    pr_number = pr_url.split("/")[-1] if pr_url else "unknown"
    print(f"PR created: {pr_url}")

    # Update wiki-gaps.md: replace "pr: pending" with actual PR number
    gaps_file = Path("content/wiki-gaps.md")
    if gaps_file.exists():
        updated = gaps_file.read_text(encoding="utf-8").replace("pr: pending", f"pr: {pr_number}")
        if updated != gaps_file.read_text(encoding="utf-8"):
            gaps_file.write_text(updated, encoding="utf-8")
            run(["git", "add", "content/wiki-gaps.md"])
            run(["git", "commit", "-m", f"wiki: PR-Nummer {pr_number} in wiki-gaps.md eingetragen"])
            run(["git", "push", "origin", branch])
            # Update the open PR with the new commit (already on same branch, no action needed)


if __name__ == "__main__":
    main()
