#!/usr/bin/env python3
"""Web search restricted to allowed sites from search_sites.txt."""

import re
from pathlib import Path

SITES_FILE = Path(__file__).parent / "search_sites.txt"

MAX_SEARCH_TERMS = 3
MAX_PREFERRED_SOURCES = 5
MAX_RESULTS_TOTAL = 6

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


def _build_queries(gap: dict) -> list[str]:
    """Build search queries from gap suchbegriffe, falling back to title."""
    suchbegriffe = gap.get("suchbegriffe", [])
    if suchbegriffe:
        return suchbegriffe[:MAX_SEARCH_TERMS]
    title = gap.get("title", "")
    title = re.sub(r"[–:]+", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    return [title]


def _get_preferred_sites(gap: dict, global_preferred: list[str]) -> list[str]:
    """Use gap's bevorzugte_quellen if set, otherwise fall back to global preferred."""
    gap_preferred = gap.get("bevorzugte_quellen", [])
    if gap_preferred:
        return gap_preferred[:MAX_PREFERRED_SOURCES]
    return global_preferred


def _collect_fact_terms(gap: dict) -> list[str]:
    """Collect relevant terms from gap criteria and search terms for fact extraction."""
    terms: list[str] = []
    for c in gap.get("akzeptanzkriterien", []):
        terms.extend(c.get("terms", []))
        terms.extend(c.get("contains", []))
    terms.extend(gap.get("suchbegriffe", []))
    terms.extend(gap.get("faktenmuster", []))
    return [t.lower() for t in terms if t]


def extract_key_facts(results: list[dict], gap: dict | None = None) -> str:
    """Extract concrete facts from snippets based on gap terms and generic patterns."""
    facts: list[str] = []

    gap_terms = _collect_fact_terms(gap) if gap else []
    # Generic patterns: percentages, multipliers, version numbers
    generic_pattern = re.compile(r"\d+\s*%|\d+x|v\d+\.\d+", re.I)

    for r in results:
        body = r.get("body", "")
        domain = r.get("href", "").split("/")[2] if r.get("href") else "?"
        for sentence in re.split(r"(?<=[.!?])\s+", body):
            s_lower = sentence.lower()
            has_generic = bool(generic_pattern.search(sentence))
            has_term = any(t in s_lower for t in gap_terms) if gap_terms else False
            if (has_generic or has_term) and len(sentence) > 30:
                facts.append(f"- {domain}: {sentence.strip()}")
                break

    return "\n".join(facts)


def search(gap: dict, max_results: int = MAX_RESULTS_TOTAL) -> list[dict]:
    """Search DuckDuckGo restricted to allowed sites. Returns filtered results."""
    global_preferred, fallback = load_sites()
    preferred = _get_preferred_sites(gap, global_preferred)
    all_sites = preferred + [s for s in fallback if s not in preferred]

    if not all_sites:
        print("  Keine Sites in search_sites.txt — Suche übersprungen.")
        return []

    try:
        from ddgs import DDGS
    except ImportError:
        print("  ddgs fehlt: pip install ddgs")
        return []

    queries = _build_queries(gap)
    site_filter = " OR ".join(f"site:{s}" for s in all_sites)

    all_results: list[dict] = []
    seen_urls: set[str] = set()

    for query in queries:
        if len(all_results) >= max_results:
            break
        full_query = f"{query} {site_filter}"
        print(f"  Suche: {full_query!r}")
        try:
            with DDGS() as ddgs:
                raw = list(ddgs.text(full_query, max_results=max_results))
            for r in raw:
                url = r.get("href", "")
                if not _is_ad(r) and url not in seen_urls:
                    seen_urls.add(url)
                    all_results.append(r)
                    if len(all_results) >= max_results:
                        break
            filtered = len(raw) - sum(1 for r in raw if r.get("href") in seen_urls or _is_ad(r))
            if filtered > 0:
                print(f"  {filtered} Werbeeintrag/Weiterleitung herausgefiltert.")
        except Exception as exc:
            print(f"  Suchfehler bei '{query}': {exc}")

    print(f"  {len(all_results)} Ergebnis(se) gefunden.")
    return all_results[:max_results]


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
    print(extract_key_facts(results, gap))
