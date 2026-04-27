#!/usr/bin/env python3
"""Apply the most recently generated patch from .runs/ without re-calling Ollama."""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiki_apply_patch import apply_patch
from wiki_validate import validate

RUNS_DIR = Path(".runs/wiki-agent")
GAPS_FILE = Path("content/wiki-gaps.md")


def find_latest_run() -> Path | None:
    candidates = sorted(
        (p.parent for p in RUNS_DIR.rglob("generated.md")),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def parse_gap_md(text: str) -> dict:
    gap: dict = {}
    for line in text.split("\n"):
        for key in ("Title", "Target", "Mode", "Heading"):
            if line.startswith(f"**{key}:**"):
                gap[key.lower()] = line.split(":", 1)[1].strip()
    return gap


def update_gap_status(content: str, title: str, new_status: str) -> str:
    lines = content.split("\n")
    in_gap = False
    updated: list[str] = []
    for line in lines:
        if line.startswith("### ") and line[4:].strip() == title:
            in_gap = True
            updated.append(line)
            continue
        if in_gap and line.startswith("status:"):
            updated.append(f"status: {new_status}")
            in_gap = False
            continue
        updated.append(line)
    return "\n".join(updated)


def main() -> None:
    run_dir = find_latest_run()
    if not run_dir:
        print("Keine generierten Runs gefunden in .runs/")
        sys.exit(1)

    print(f"Neuester Run: {run_dir}")

    gap_md = run_dir / "gap.md"
    generated_md = run_dir / "generated.md"

    if not gap_md.exists() or not generated_md.exists():
        print("gap.md oder generated.md fehlen im Run-Verzeichnis.")
        sys.exit(1)

    gap = parse_gap_md(gap_md.read_text(encoding="utf-8"))
    generated = generated_md.read_text(encoding="utf-8")

    print(f"Gap:    {gap.get('title', '?')}")
    print(f"Target: {gap.get('target', '?')}")
    print(f"Mode:   {gap.get('mode', '?')}  |  Heading: {gap.get('heading', '?')}")

    errors, warnings = validate(generated, gap)
    for e in errors:
        print(f"  ERROR: {e}")
    for w in warnings:
        print(f"  WARN:  {w}")

    if errors:
        print("\nValidierung fehlgeschlagen. Patch nicht angewendet.")
        sys.exit(1)

    target_path = Path(gap["target"])
    updated = apply_patch(
        target_path.read_text(encoding="utf-8"),
        generated,
        gap["heading"],
        gap["mode"],
    )

    if updated is None:
        print(f"  Heading nicht gefunden: {gap['heading']!r}")
        sys.exit(1)

    target_path.write_text(updated, encoding="utf-8")

    if GAPS_FILE.exists():
        gaps_content = GAPS_FILE.read_text(encoding="utf-8")
        gaps_content = update_gap_status(gaps_content, gap.get("title", ""), "applied")
        GAPS_FILE.write_text(gaps_content, encoding="utf-8")

    diff = subprocess.run(["git", "diff", str(target_path)], capture_output=True, text=True)
    if diff.stdout:
        print(f"\n--- git diff ---\n{diff.stdout[:4000]}")

    print(f"\nPatch angewendet. Prüfe den Diff oben, dann: 4_commit_push.bat")


if __name__ == "__main__":
    main()
