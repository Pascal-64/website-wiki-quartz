#!/usr/bin/env python3
"""Parse content/wiki-gaps.md and return open gap items."""

from pathlib import Path

GAPS_FILE = Path("content/wiki-gaps.md")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def parse_gaps(content: str) -> list[dict]:
    """Parse gap blocks from wiki-gaps.md content. Returns only open items."""
    gaps = []
    current = None
    in_section = False
    in_aufgabe = False
    in_kriterien = False
    aufgabe_lines: list[str] = []
    kriterien_lines: list[str] = []

    for line in content.split("\n"):
        if line.startswith("## Offene Lücken"):
            in_section = True
            continue
        if in_section and line.startswith("## ") and not line.startswith("### "):
            in_section = False
            if current:
                current["aufgabe"] = "\n".join(aufgabe_lines).strip()
                current["kriterien"] = [k for k in kriterien_lines if k]
                gaps.append(current)
                current = None
            continue

        if not in_section:
            continue

        if line.startswith("### "):
            if current:
                current["aufgabe"] = "\n".join(aufgabe_lines).strip()
                current["kriterien"] = [k for k in kriterien_lines if k]
                gaps.append(current)
            current = {
                "title": line[4:].strip(),
                "status": "open",
                "priority": "medium",
                "target": "",
                "mode": "append_under_heading",
                "heading": "",
                "aufgabe": "",
                "kriterien": [],
            }
            in_aufgabe = False
            in_kriterien = False
            aufgabe_lines = []
            kriterien_lines = []
            continue

        if current is None:
            continue

        if line.strip() == "---":
            continue

        if line.strip() == "Aufgabe:":
            in_aufgabe = True
            in_kriterien = False
            continue

        if line.strip() == "Akzeptanzkriterien:":
            in_aufgabe = False
            in_kriterien = True
            continue

        if in_kriterien:
            stripped = line.strip()
            if stripped.startswith("- "):
                kriterien_lines.append(stripped[2:].strip())
            continue

        if in_aufgabe:
            aufgabe_lines.append(line)
            continue

        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"')
            if key in ("status", "priority", "target", "mode", "heading"):
                current[key] = val

    if current:
        current["aufgabe"] = "\n".join(aufgabe_lines).strip()
        current["kriterien"] = [k for k in kriterien_lines if k]
        gaps.append(current)

    open_gaps = [g for g in gaps if g["status"] == "open"]
    open_gaps.sort(key=lambda x: PRIORITY_ORDER.get(x["priority"], 1))
    return open_gaps


def load_gaps() -> list[dict]:
    if not GAPS_FILE.exists():
        return []
    return parse_gaps(GAPS_FILE.read_text(encoding="utf-8"))


if __name__ == "__main__":
    for gap in load_gaps():
        k = gap.get("kriterien", [])
        print(f"[{gap['priority']}] {gap['title']} → {gap['target']}  ({len(k)} Kriterien)")
