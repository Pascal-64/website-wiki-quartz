#!/usr/bin/env python3
"""
Enrich generated markdown with internal wikilinks.

Scans all wiki pages, finds those whose names appear in the generated text,
and appends a '## Siehe auch' section with matching [[wikilinks]].

Usage:
  python scripts/wiki_enrich_links.py --run .runs/wiki-agent/2026-04-27/007
  python scripts/wiki_enrich_links.py --run .runs/.../007 --dry-run
"""

import argparse
import re
import sys
from pathlib import Path

CONTENT_DIR = Path("content")
SKIP_FILES = {"index.md", "wiki-gaps.md"}
MIN_NAME_LENGTH = 2


def _frontmatter_title(text: str) -> str | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    for line in text[3:end].split("\n"):
        if line.startswith("title:"):
            return line[6:].strip().strip("\"'")
    return None


def _first_h1(text: str) -> str | None:
    for line in text.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _stem_to_display(stem: str) -> str:
    return stem.replace("-", " ").replace("_", " ")


def build_page_index(exclude_path: Path | None = None) -> list[dict]:
    """Return list of {display_name, match_names, path} for all wiki pages."""
    pages: list[dict] = []
    for md_path in CONTENT_DIR.rglob("*.md"):
        if md_path.name in SKIP_FILES:
            continue
        if exclude_path and md_path.resolve() == exclude_path.resolve():
            continue

        text = md_path.read_text(encoding="utf-8")
        stem = md_path.stem
        stem_display = _stem_to_display(stem)
        fm_title = _frontmatter_title(text)
        h1 = _first_h1(text)

        display = fm_title or h1 or stem_display

        # Collect unique match candidates, longest first (avoid short shadowing long)
        seen: set[str] = set()
        match_names: list[str] = []
        for name in [fm_title, h1, stem_display, stem]:
            if name and name.lower() not in seen and len(name) >= MIN_NAME_LENGTH:
                match_names.append(name)
                seen.add(name.lower())

        pages.append({"display": display, "match_names": match_names, "path": md_path})

    # Sort by longest display name first to prevent short names masking longer ones
    pages.sort(key=lambda p: len(p["display"]), reverse=True)
    return pages


def find_matching_pages(generated: str, pages: list[dict]) -> list[dict]:
    """Return pages whose names appear in the generated text (not already linked)."""
    already = {
        m.lower()
        for m in re.findall(r"\[\[([^\|\]]+)(?:\|[^\]]+)?\]\]", generated)
    }

    matched: list[dict] = []
    for page in pages:
        if page["display"].lower() in already:
            continue
        if any(n.lower() in already for n in page["match_names"]):
            continue

        for name in page["match_names"]:
            pattern = r"(?<![#\[\w])\b" + re.escape(name) + r"\b(?!\])"
            if re.search(pattern, generated, re.IGNORECASE):
                matched.append(page)
                break

    return matched


def enrich(generated: str, gap: dict) -> tuple[str, list[str]]:
    """
    Append '## Siehe auch' section with matching wikilinks.
    Returns (enriched_text, added_links).
    If no matches or section already exists, returns original text unchanged.
    """
    target_path = Path(gap.get("target", ""))
    exclude = target_path if target_path.name else None
    pages = build_page_index(exclude_path=exclude)
    matched = find_matching_pages(generated, pages)

    if not matched:
        return generated, []

    if re.search(r"^##\s+Siehe auch", generated, re.MULTILINE | re.IGNORECASE):
        return generated, []

    # Don't add if target file already has a Siehe auch section (validator would block it)
    if exclude and exclude.exists():
        target_text = exclude.read_text(encoding="utf-8")
        if re.search(r"^##\s+Siehe auch", target_text, re.MULTILINE | re.IGNORECASE):
            return generated, []

    links = [f"[[{p['display']}]]" for p in matched]
    section = "\n\n## Siehe auch\n\n" + "\n".join(f"- {lnk}" for lnk in links)

    return generated.rstrip() + section + "\n", links


def main() -> None:
    parser = argparse.ArgumentParser(description="Enrich generated.md with wikilinks")
    parser.add_argument("--run", type=Path, required=True,
                        help="Run-Verzeichnis mit generated.md und gap.md")
    parser.add_argument("--dry-run", action="store_true",
                        help="Zeige gefundene Links, schreibe nichts")
    args = parser.parse_args()

    run_dir = args.run
    gen_path = run_dir / "generated.md"
    gap_path = run_dir / "gap.md"

    if not gen_path.exists():
        print(f"Fehler: {gen_path} nicht gefunden.")
        sys.exit(1)

    generated = gen_path.read_text(encoding="utf-8")

    gap: dict = {}
    if gap_path.exists():
        sys.path.insert(0, str(Path(__file__).parent))
        from wiki_apply_run import parse_gap_md
        gap = parse_gap_md(gap_path.read_text(encoding="utf-8"))

    enriched, links = enrich(generated, gap)

    if not links:
        print("Keine passenden Wiki-Seiten gefunden.")
        return

    print(f"Gefundene Links ({len(links)}):")
    for lnk in links:
        print(f"  {lnk}")

    if args.dry_run:
        print("\n[Dry-Run] generated.md nicht verändert.")
        return

    gen_path.write_text(enriched, encoding="utf-8")
    print(f"\ngespeichert: {gen_path}")


if __name__ == "__main__":
    main()
