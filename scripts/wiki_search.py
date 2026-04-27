#!/usr/bin/env python3
"""Web search restricted to allowed sites from search_sites.txt."""

import re
from pathlib import Path

SITES_FILE = Path(__file__).parent / "search_sites.txt"

AD_URL_PATTERNS = (
    "bing.com/aclick",
    "bing.com/aclk",
    "google.com/aclk",
    "doubleclick.net",
    "googleadservices.com",
    "/aclick?",
    "?ld=",
    "sponsored",
    "utm_source=ads",
    "/pricing",
    "/checkout",
)


def load_sites() -> tuple[list[str], list[str]]:
    """Returns (preferred_sites, fallback_sites) from search_sites.txt."""
    if not SITES_FILE.exists():
        return [], []

    preferred: list[str] = []
    fallback: list[str] = []
    section = "fallback"

    for line in SITES_FILE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            if "bevorzugt" in stripped.lower() or "preferred" in stripped.lower():
                section = "preferred"
            elif "fallback" in stripped.lower() or "erlaubt" in stripped.lower():
                section = "fallback"
            continue
        if section == "preferred":
            preferred.append(stripped)
        else:
            fallback.append(stripped)

    return preferred, fallback


def _is_ad(result: dict) -> bool:
    url = result.get("href", "").lower()
    return any(p in url for p in AD_URL_PATTERNS)


def _build_query(gap: dict) -> str:
    title = gap.get("title", "")
    title = re.sub(r"[–:]+", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title


def extract_key_facts(results: list[dict]) -> str:
    """Extract concrete, measurable facts from snippets (numbers, specific claims)."""
    facts: list[str] = []
    fact_pattern = re.compile(
        r"\d+\s*%|\d+x|\bconsumer\b|\bhardware\b|\bmemory\b|\bparameter\b|"
        r"\bloraconfig\b|\bpeft\b|\breward model\b|\bdpo\b|\bqlora\b",
        re.I,
    )
    for r in results:
        body = r.get("body", "")
        domain = r.get("href", "").split("/")[2] if r.get("href") else "?"
        for sentence in re.split(r"(?<=[.!?])\s+", body):
            if fact_pattern.search(sentence) and len(sentence) > 30:
                facts.append(f"- {domain}: {sentence.strip()}")
                break
    return "\n".join(facts)


def search(gap: dict, max_results: int = 6) -> list[dict]:
    """Search DuckDuckGo restricted to allowed sites. Returns filtered results."""
    preferred, fallback = load_sites()
    all_sites = preferred + [s for s in fallback if s not in preferred]

    if not all_sites:
        print("  Keine Sites in search_sites.txt — Suche übersprungen.")
        return []

    try:
        from ddgs import DDGS
    except ImportError:
        print("  ddgs fehlt: pip install ddgs")
        return []

    query = _build_query(gap)
    site_filter = " OR ".join(f"site:{s}" for s in all_sites)
    full_query = f"{query} {site_filter}"

    print(f"  Suche: {full_query!r}")
    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(full_query, max_results=max_results))
        results = [r for r in raw if not _is_ad(r)][:4]
        filtered = len(raw) - len(results)
        if filtered:
            print(f"  {filtered} Werbeeintrag/Weiterleitung herausgefiltert.")
        print(f"  {len(results)} Ergebnis(se) gefunden.")
        return results
    except Exception as exc:
        print(f"  Suchfehler: {exc}")
        return []


def format_results(results: list[dict]) -> str:
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
    print("\n--- Ergebnisse ---")
    print(format_results(results))
    print("\n--- Key Facts ---")
    print(extract_key_facts(results))
