#!/usr/bin/env python3
"""
Local wiki gap filling agent using Ollama.

Usage:
  # Dry-run (generates only, does NOT touch content/):
  python scripts/wiki_agent_local.py --max-gaps 1 --model qwen2.5-coder:14b

  # Generate + apply:
  python scripts/wiki_agent_local.py --max-gaps 1 --model qwen2.5-coder:14b --apply

  # Generate + apply + commit (no push):
  python scripts/wiki_agent_local.py --max-gaps 1 --model qwen2.5-coder:14b --apply --commit
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import ollama

from wiki_apply_patch import apply_patch
from wiki_context import build_context
from wiki_detect_gaps import parse_gaps
from wiki_search import format_results, search
from wiki_validate import validate

CONTENT_DIR = Path("content")
GAPS_FILE = CONTENT_DIR / "wiki-gaps.md"
RUNS_DIR = Path(".runs/wiki-agent")

SYSTEM_PROMPT = """\
Du erweiterst ein deutsches Technik-Wiki im Obsidian/Quartz-Format.

Gib ausschließlich den neuen Markdown-Abschnitt zurück.

Regeln:
- Beginne direkt mit der Überschrift in der erwarteten Ebene (steht explizit im Prompt).
- Keine Einleitung, kein "Hier ist", kein "Gerne", kein "Natürlich".
- Kein Markdown-Codeblock um die gesamte Antwort.
- Kein JSON, kein HTML.
- Keine Wiederholung bestehender Abschnitte.
- Mathematik: $...$ (inline) und $$...$$ (Block). KEIN \\(...\\) oder \\[...\\].
- Heading-Ebene: Eine Ebene tiefer als das Ziel-Heading. Die erwartete Ebene steht im Prompt.
- Wikilinks im Format [[Seitenname]] nur wenn sinnvoll.
- Schreibe auf Deutsch.\
"""

TRANSIENT_KEYWORDS = (
    "connection refused", "max retries exceeded",
    "read timed out", "connecterror", "connectionerror",
    "failed to connect",
)


def make_run_dir() -> Path:
    today = date.today().isoformat()
    base = RUNS_DIR / today
    base.mkdir(parents=True, exist_ok=True)
    existing = [d for d in base.iterdir() if d.is_dir()]
    run_dir = base / f"{len(existing) + 1:03d}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def build_user_prompt(gap: dict, ctx: dict) -> str:
    heading = gap.get("heading", "").strip('"').strip()
    m = re.match(r"^(#+)\s", heading)
    target_level = len(m.group(1)) if m else 2
    expected_prefix = "#" * (target_level + 1)

    parts: list[str] = []

    if ctx.get("style_guide"):
        parts.append(f"## Style-Referenz\n\n{ctx['style_guide']}")

    parts.append(f"## Aufgabe\n\n{ctx.get('task', gap['title'])}")

    if ctx.get("search_results"):
        parts.append(f"## Recherche-Ergebnisse\n\n{ctx['search_results']}")

    parts.append(
        f"## Zieldatei\n\n"
        f"Datei: {gap['target']}\n"
        f"Einfügemodus: {gap['mode']}\n"
        f"Ziel-Heading: {gap['heading']}\n"
        f"Erwartete Heading-Ebene für neuen Abschnitt: `{expected_prefix}` "
        f"(eine Ebene tiefer als Ziel-Heading)"
    )

    parts.append(
        f"## Kontext aus der Zieldatei\n\n"
        f"### Frontmatter\n{ctx.get('frontmatter', '')}\n\n"
        f"### Überschriftenstruktur\n{ctx.get('headings', '')}\n\n"
        f"### Relevanter Abschnitt\n{ctx.get('target_section', '')}"
    )

    if ctx.get("known_pages"):
        parts.append(f"## Bekannte Wiki-Seiten\n\n{ctx['known_pages']}")

    parts.append(
        f"Erzeuge jetzt nur den neuen Markdown-Abschnitt. "
        f"Beginne mit einer `{expected_prefix}` Überschrift."
    )

    return "\n\n---\n\n".join(parts)


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
    parser = argparse.ArgumentParser(description="Local wiki gap filling agent")
    parser.add_argument("--max-gaps", type=int, default=1)
    parser.add_argument("--model", default="qwen2.5-coder:14b")
    parser.add_argument("--apply", action="store_true", help="Apply patch to content/")
    parser.add_argument("--commit", action="store_true", help="Create git commit (requires --apply)")
    parser.add_argument("--no-search", action="store_true", help="Skip web search")
    args = parser.parse_args()

    if args.commit and not args.apply:
        print("Error: --commit requires --apply", file=sys.stderr)
        sys.exit(1)

    if not GAPS_FILE.exists():
        print(f"wiki-gaps.md not found at {GAPS_FILE}")
        sys.exit(0)

    gaps_content = GAPS_FILE.read_text(encoding="utf-8")
    gaps = parse_gaps(gaps_content)

    if not gaps:
        print("No open gaps found.")
        sys.exit(0)

    to_process = gaps[: args.max_gaps]
    print(f"Processing {len(to_process)} gap(s) with model {args.model}")
    if not args.apply:
        print("Mode: DRY-RUN (use --apply to modify content/)\n")

    for gap in to_process:
        print(f"\n{'=' * 60}")
        print(f"Gap:    {gap['title']}")
        print(f"Target: {gap['target']}")
        print(f"Mode:   {gap['mode']}  |  Heading: {gap['heading']}")

        run_dir = make_run_dir()
        print(f"Run:    {run_dir}")

        (run_dir / "gap.md").write_text(
            f"# Gap\n\n"
            f"**Title:** {gap['title']}\n"
            f"**Target:** {gap['target']}\n"
            f"**Mode:** {gap['mode']}\n"
            f"**Heading:** {gap['heading']}\n\n"
            f"**Aufgabe:**\n{gap.get('aufgabe', '')}\n",
            encoding="utf-8",
        )

        ctx = build_context(gap)

        if not args.no_search:
            print("  Web-Suche läuft...")
            search_results = search(gap)
            ctx["search_results"] = format_results(search_results)
            (run_dir / "sources.md").write_text(
                f"# Recherche-Ergebnisse\n\n{ctx['search_results']}\n", encoding="utf-8"
            )
        else:
            ctx["search_results"] = ""

        (run_dir / "context.md").write_text(
            f"# Context\n\n"
            f"## Frontmatter\n{ctx.get('frontmatter', '')}\n\n"
            f"## Headings\n{ctx.get('headings', '')}\n\n"
            f"## Target Section\n{ctx.get('target_section', '')}\n\n"
            f"## Known Pages\n{ctx.get('known_pages', '')}\n",
            encoding="utf-8",
        )

        user_prompt = build_user_prompt(gap, ctx)
        (run_dir / "prompt.md").write_text(
            f"# System Prompt\n\n{SYSTEM_PROMPT}\n\n---\n\n# User Prompt\n\n{user_prompt}\n",
            encoding="utf-8",
        )

        print(f"Calling Ollama ({args.model})...", flush=True)
        try:
            response = ollama.generate(
                model=args.model,
                system=SYSTEM_PROMPT,
                prompt=user_prompt,
                stream=False,
            )
            generated: str = response["response"]
        except Exception as exc:
            err_lower = str(exc).lower()
            is_transient = any(k in err_lower for k in TRANSIENT_KEYWORDS)
            if is_transient:
                print("  Verbindungsfehler (transient) — Status bleibt 'open'. Ist Ollama gestartet?", file=sys.stderr)
            else:
                print(f"  Fehler: {exc}", file=sys.stderr)
                if args.apply:
                    gaps_content = update_gap_status(gaps_content, gap["title"], "failed")
                    GAPS_FILE.write_text(gaps_content, encoding="utf-8")
            (run_dir / "result.log").write_text(
                f"{'TRANSIENT' if is_transient else 'FAILED'}: {exc}\n", encoding="utf-8"
            )
            continue

        (run_dir / "generated.md").write_text(generated, encoding="utf-8")
        print(f"  Generated {len(generated)} chars.")

        errors, warnings = validate(generated, gap)
        log_lines: list[str] = []

        if errors:
            log_lines.append("ERRORS:")
            log_lines.extend(f"  - {e}" for e in errors)
        if warnings:
            log_lines.append("WARNINGS:")
            log_lines.extend(f"  - {w}" for w in warnings)
        if not errors and not warnings:
            log_lines.append("OK: No issues.")

        for e in errors:
            print(f"  ERROR: {e}")
        for w in warnings:
            print(f"  WARN:  {w}")

        if errors:
            (run_dir / "result.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
            if args.apply:
                gaps_content = update_gap_status(gaps_content, gap["title"], "failed")
                GAPS_FILE.write_text(gaps_content, encoding="utf-8")
            continue

        if not args.apply:
            log_lines.append("\nDRY-RUN: content/ not modified. Run 3_apply.bat to apply.")
            (run_dir / "result.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
            print(f"  Dry-run done. See: {run_dir / 'generated.md'}")
            continue

        target_path = Path(gap["target"])
        file_content = target_path.read_text(encoding="utf-8")
        updated = apply_patch(file_content, generated, gap["heading"], gap["mode"])

        if updated is None:
            msg = f"Apply FAILED: heading not found: {gap['heading']!r}"
            print(f"  {msg}")
            log_lines.append(msg)
            (run_dir / "result.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
            gaps_content = update_gap_status(gaps_content, gap["title"], "failed")
            GAPS_FILE.write_text(gaps_content, encoding="utf-8")
            continue

        target_path.write_text(updated, encoding="utf-8")
        gaps_content = update_gap_status(gaps_content, gap["title"], "applied")
        GAPS_FILE.write_text(gaps_content, encoding="utf-8")

        diff = subprocess.run(
            ["git", "diff", str(target_path)], capture_output=True, text=True
        )
        if diff.stdout:
            (run_dir / "diff.patch").write_text(diff.stdout, encoding="utf-8")
            print(f"  Patch applied. Diff:\n")
            print(diff.stdout[:3000])

        log_lines.append(f"\nAPPLIED: {target_path}")
        (run_dir / "result.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")

        if args.commit:
            md_files = list(CONTENT_DIR.rglob("*.md"))
            subprocess.run(["git", "add"] + [str(f) for f in md_files], check=True)
            commit_msg = f"Add wiki content: {gap['title']}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            print(f"  Committed: {commit_msg}")

    print(f"\nDone. Push manually with: git push")


if __name__ == "__main__":
    main()
