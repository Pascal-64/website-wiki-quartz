#!/usr/bin/env python3
"""Web search restricted to allowed sites from search_sites.txt."""

import re
from pathlib import Path

SITES_FILE = Path(__file__).parent / "search_sites.txt"


def load_sites() -> list[str]:
    if not SITES_FILE.exists():
        return []
    return [
        line.strip()
        for line in SITES_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]


def _build_query(gap: dict) -> str:
    title = gap.get("title", "")
    title = re.sub(r"[–:]+", " ", title)       # em-dash und Doppelpunkt entfernen, Bindestriche behalten
    title = re.sub(r"\s+", " ", title).strip()  # mehrfache Leerzeichen zusammenführen
    return title


def search(gap: dict, max_results: int = 4) -> list[dict]:
    """Search DuckDuckGo restricted to allowed sites. Returns list of result dicts."""
    sites = load_sites()
    if not sites:
        print("  Keine Sites in search_sites.txt — Suche übersprungen.")
        return []

    try:
        from ddgs import DDGS
    except ImportError:
        print("  ddgs fehlt: pip install ddgs")
        return []

    query = _build_query(gap)
    site_filter = " OR ".join(f"site:{s}" for s in sites)
    full_query = f"{query} {site_filter}"

    print(f"  Suche: {full_query!r}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(full_query, max_results=max_results))
        print(f"  {len(results)} Ergebnis(se) gefunden.")
        return results
    except Exception as exc:
        print(f"  Suchfehler: {exc}")
        return []


def format_results(results: list[dict]) -> str:
    """Format search results as markdown block for the prompt."""
    if not results:
        return ""
    lines: list[str] = []
    for i, r in enumerate(results, 1):
        lines.append(f"### Quelle {i}: {r.get('title', 'Kein Titel')}")
        lines.append(f"URL: {r.get('href', '')}")
        lines.append(r.get("body", "").strip())
        lines.append("")
    return "\n".join(lines).strip()


if __name__ == "__main__":
    import sys
    gap = {"title": sys.argv[1] if len(sys.argv) > 1 else "LoRA Fine-Tuning"}
    results = search(gap)
    print(format_results(results))
