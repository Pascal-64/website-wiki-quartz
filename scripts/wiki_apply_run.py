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
from wiki_detect_gaps import load_all_gaps
from wiki_validate import validate, check_structured_criteria

RUNS_DIR = Path(".runs/wiki-agent")
GAPS_FILE = Path("content/wiki-gaps.md")


def collect_runs() -> list[Path]:
    return sorted(
        (p.parent for p in RUNS_DIR.rglob("generated.md")),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )


_gap_cache: list[dict] | None = None


def _get_all_gaps() -> list[dict]:
    global _gap_cache
    if _gap_cache is None:
        _gap_cache = load_all_gaps()
    return _gap_cache


def _find_gap_by_title(title: str) -> dict | None:
    title_lower = title.lower().strip()
    for g in _get_all_gaps():
        if g.get("title", "").lower().strip() == title_lower:
            return g
    return None


def run_metrics(run_dir: Path) -> dict:
    gen = run_dir / "generated.md"
    sources = run_dir / "sources.md"
    result_log = run_dir / "result.log"
    gap_file = run_dir / "gap.md"

    text = gen.read_text(encoding="utf-8") if gen.exists() else ""
    sources_text = sources.read_text(encoding="utf-8") if sources.exists() else ""
    result_text = result_log.read_text(encoding="utf-8") if result_log.exists() else ""

    criteria_met = 0
    criteria_total = 0
    num_errors = 0
    num_warnings = 0

    if text and gap_file.exists():
        gap_data = parse_gap_md(gap_file.read_text(encoding="utf-8"))
        gap_title = gap_data.get("title", "")
        full_gap = _find_gap_by_title(gap_title) if gap_title else None
        if full_gap:
            errors, warnings = validate(text, full_gap, sources_text)
            num_errors = len(errors)
            num_warnings = len(warnings)
            ak = full_gap.get("akzeptanzkriterien", [])
            required = [c for c in ak if c.get("required", True)]
            criteria_total = len(required)
            if criteria_total > 0:
                unmet = check_structured_criteria(text, full_gap, sources_text)
                criteria_met = criteria_total - len(unmet)

    return {
        "chars": len(text),
        "has_code": "```python" in text,
        "has_table": "|---|" in text or "| ---" in text,
        "source_count": sources_text.count("### Quelle"),
        "ok": bool(text) and "ERRORS:" not in result_text and "FAILED:" not in result_text,
        "criteria_met": criteria_met,
        "criteria_total": criteria_total,
        "errors": num_errors,
        "warnings": num_warnings,
    }


def print_runs(runs: list[Path]) -> None:
    header = f"{'Nr':>3}  {'Run':<30}  {'Zeichen':>7}  {'Kriterien':>9}  {'Err':>3}  {'Warn':>4}  {'Qu.':>3}  {'Code':<5}  {'Tab.':<5}  Status"
    print(f"\n{header}")
    print("-" * len(header))
    for i, run_dir in enumerate(runs):
        m = run_metrics(run_dir)
        label = "/".join(run_dir.parts[-3:])
        status = "OK  " if m["ok"] else "FAIL"
        code = "ja" if m["has_code"] else "nein"
        tab = "ja" if m["has_table"] else "nein"
        if m["criteria_total"] > 0:
            crit = f"{m['criteria_met']}/{m['criteria_total']}"
        else:
            crit = "–"
        print(
            f"{i+1:>3}  {label:<30}  {m['chars']:>7}  {crit:>9}  "
            f"{m['errors']:>3}  {m['warnings']:>4}  {m['source_count']:>3}  "
            f"{code:<5}  {tab:<5}  {status}"
        )
    print()


def parse_gap_md(text: str) -> dict:
    gap: dict = {}
    for line in text.split("\n"):
        for key in ("Title", "Target", "Mode", "Heading"):
            prefix = f"**{key}:**"
            if line.startswith(prefix):
                gap[key.lower()] = line[len(prefix):].strip()
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
