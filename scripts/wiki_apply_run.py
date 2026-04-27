#!/usr/bin/env python3
"""
Apply a specific run by path, or list available runs with metrics and let user choose.

Usage:
  python scripts/wiki_apply_run.py                          # list + interactive select
  python scripts/wiki_apply_run.py --run .runs/.../005      # apply directly
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from wiki_apply_patch import apply_patch
from wiki_validate import validate

RUNS_DIR = Path(".runs/wiki-agent")
GAPS_FILE = Path("content/wiki-gaps.md")


def collect_runs() -> list[Path]:
    return sorted(
        (p.parent for p in RUNS_DIR.rglob("generated.md")),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )


def run_metrics(run_dir: Path) -> dict:
    gen = run_dir / "generated.md"
    sources = run_dir / "sources.md"
    result_log = run_dir / "result.log"

    text = gen.read_text(encoding="utf-8") if gen.exists() else ""
    sources_text = sources.read_text(encoding="utf-8") if sources.exists() else ""
    result_text = result_log.read_text(encoding="utf-8") if result_log.exists() else ""

    return {
        "chars": len(text),
        "has_code": "```python" in text,
        "has_table": "|---|" in text or "| ---" in text,
        "source_count": sources_text.count("### Quelle"),
        "ok": bool(text) and "ERRORS:" not in result_text and "FAILED:" not in result_text,
    }


def print_runs(runs: list[Path]) -> None:
    print(f"\n{'Nr':>3}  {'Run':<30}  {'Zeichen':>7}  {'Code':<5}  {'Tab.':<5}  {'Qu.':>3}  Status")
    print("-" * 68)
    for i, run_dir in enumerate(runs):
        m = run_metrics(run_dir)
        label = "/".join(run_dir.parts[-3:])
        status = "OK  " if m["ok"] else "FAIL"
        code = "ja" if m["has_code"] else "nein"
        tab = "ja" if m["has_table"] else "nein"
        print(f"{i+1:>3}  {label:<30}  {m['chars']:>7}  {code:<5}  {tab:<5}  {m['source_count']:>3}  {status}")
    print()


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


def apply_run(run_dir: Path) -> None:
    run_dir = Path(run_dir)
    gap_md = run_dir / "gap.md"
    generated_md = run_dir / "generated.md"

    if not gap_md.exists() or not generated_md.exists():
        print(f"gap.md oder generated.md fehlen in: {run_dir}")
        sys.exit(1)

    gap = parse_gap_md(gap_md.read_text(encoding="utf-8"))
    generated = generated_md.read_text(encoding="utf-8")

    print(f"\nGap:    {gap.get('title', '?')}")
    print(f"Target: {gap.get('target', '?')}")
    print(f"Run:    {run_dir}")

    errors, warnings = validate(generated, gap)
    for e in errors:
        print(f"  ERROR: {e}")
    for w in warnings:
        print(f"  WARN:  {w}")

    if errors:
        print("\nValidierung fehlgeschlagen — nicht angewendet.")
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
        (run_dir / "diff.patch").write_text(diff.stdout, encoding="utf-8")
        print(f"\n--- git diff ---\n{diff.stdout[:4000]}")

    print(f"\nAngewendet. Wenn Diff ok: 4_commit_push.bat")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply a specific wiki run")
    parser.add_argument("--run", type=Path, default=None,
                        help="Run-Verzeichnis (z.B. .runs/wiki-agent/2026-04-27/005)")
    args = parser.parse_args()

    if args.run:
        apply_run(args.run)
        return

    runs = collect_runs()
    if not runs:
        print("Keine Runs mit generated.md gefunden in .runs/")
        sys.exit(0)

    print_runs(runs)
    choice = input(f"Welchen Run anwenden? [1-{len(runs)}] oder Enter = Abbrechen: ").strip()
    if not choice:
        print("Abgebrochen.")
        sys.exit(0)

    try:
        idx = int(choice) - 1
        assert 0 <= idx < len(runs)
    except (ValueError, AssertionError):
        print("Ungültige Auswahl.")
        sys.exit(1)

    apply_run(runs[idx])


if __name__ == "__main__":
    main()
