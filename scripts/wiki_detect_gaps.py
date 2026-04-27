#!/usr/bin/env python3
"""Parse content/wiki-gaps.md and return open gap items."""

import yaml
from pathlib import Path

GAPS_FILE = Path("content/wiki-gaps.md")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def _parse_yaml_list(lines: list[str]) -> list[str]:
    """Parse collected lines as a YAML sequence, falling back to simple bullet parsing."""
    if not lines:
        return []
    text = "\n".join(lines)
    try:
        result = yaml.safe_load(text)
        if isinstance(result, list):
            return [str(item) for item in result]
    except yaml.YAMLError:
        pass
    items = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def _parse_yaml_criteria(lines: list[str]) -> tuple[list[dict], list[str]]:
    """Parse Akzeptanzkriterien lines.

    Returns (structured_criteria, legacy_criteria).
    If lines contain 'type:', parses as YAML dicts.
    Otherwise returns legacy text list.
    """
    if not lines:
        return [], []
    text = "\n".join(lines).strip()
    if not text:
        return [], []

    if "type:" in text:
        try:
            result = yaml.safe_load(text)
            if isinstance(result, list):
                return result, []
        except yaml.YAMLError:
            pass
    # Legacy: plain bullet list
    items = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return [], items


def _new_state() -> dict:
    return {
        "aufgabe_lines": [],
        "suchbegriffe_lines": [],
        "bevorzugte_quellen_lines": [],
        "faktenmuster_lines": [],
        "akzeptanzkriterien_lines": [],
        "current_section": None,
    }


def _finalize_gap(current: dict, state: dict) -> dict:
    current["aufgabe"] = "\n".join(state["aufgabe_lines"]).strip()
    current["suchbegriffe"] = _parse_yaml_list(state["suchbegriffe_lines"])
    current["bevorzugte_quellen"] = _parse_yaml_list(state["bevorzugte_quellen_lines"])
    current["faktenmuster"] = _parse_yaml_list(state["faktenmuster_lines"])
    structured, legacy = _parse_yaml_criteria(state["akzeptanzkriterien_lines"])
    current["akzeptanzkriterien"] = structured
    current["kriterien"] = legacy
    return current


def parse_gaps(content: str) -> list[dict]:
    """Parse gap blocks from wiki-gaps.md content. Returns only open items."""
    gaps = []
    current = None
    in_section = False
    state = _new_state()

    for line in content.split("\n"):
        if line.startswith("## Offene Lücken"):
            in_section = True
            continue
        if in_section and line.startswith("## ") and not line.startswith("### "):
            in_section = False
            if current:
                gaps.append(_finalize_gap(current, state))
                current = None
            continue

        if not in_section:
            continue

        if line.startswith("### "):
            if current:
                gaps.append(_finalize_gap(current, state))
            current = {
                "title": line[4:].strip(),
                "status": "open",
                "priority": "medium",
                "target": "",
                "mode": "append_under_heading",
                "heading": "",
                "aufgabe": "",
                "kriterien": [],
                "suchbegriffe": [],
                "bevorzugte_quellen": [],
                "faktenmuster": [],
                "akzeptanzkriterien": [],
            }
            state = _new_state()
            continue

        if current is None:
            continue

        if line.strip() == "---":
            continue

        stripped = line.strip()

        # Section header detection
        if stripped == "Aufgabe:":
            state["current_section"] = "aufgabe"
            continue
        if stripped == "Suchbegriffe:":
            state["current_section"] = "suchbegriffe"
            continue
        if stripped == "Bevorzugte Quellen:":
            state["current_section"] = "bevorzugte_quellen"
            continue
        if stripped == "Faktenmuster:":
            state["current_section"] = "faktenmuster"
            continue
        if stripped == "Akzeptanzkriterien:":
            state["current_section"] = "akzeptanzkriterien"
            continue

        section = state["current_section"]

        if section == "aufgabe":
            state["aufgabe_lines"].append(line)
        elif section == "suchbegriffe":
            state["suchbegriffe_lines"].append(line)
        elif section == "bevorzugte_quellen":
            state["bevorzugte_quellen_lines"].append(line)
        elif section == "faktenmuster":
            state["faktenmuster_lines"].append(line)
        elif section == "akzeptanzkriterien":
            state["akzeptanzkriterien_lines"].append(line)
        elif ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"')
            if key in ("status", "priority", "target", "mode", "heading"):
                current[key] = val

    if current:
        gaps.append(_finalize_gap(current, state))

    open_gaps = [g for g in gaps if g["status"] == "open"]
    open_gaps.sort(key=lambda x: PRIORITY_ORDER.get(x["priority"], 1))
    return open_gaps


def load_gaps() -> list[dict]:
    if not GAPS_FILE.exists():
        return []
    return parse_gaps(GAPS_FILE.read_text(encoding="utf-8"))


def load_all_gaps() -> list[dict]:
    """Load all gaps regardless of status (for metrics lookup)."""
    if not GAPS_FILE.exists():
        return []
    return _parse_all(GAPS_FILE.read_text(encoding="utf-8"))


def _parse_all(content: str) -> list[dict]:
    """Like parse_gaps but returns all statuses."""
    # Reuse parse_gaps logic but skip the open-only filter
    gaps = []
    current = None
    in_section = False
    state = _new_state()

    for line in content.split("\n"):
        if line.startswith("## Offene Lücken") or line.startswith("## Erledigt"):
            in_section = True
            continue
        if in_section and line.startswith("## ") and not line.startswith("### "):
            in_section = False
            if current:
                gaps.append(_finalize_gap(current, state))
                current = None
            continue

        if not in_section:
            continue

        if line.startswith("### "):
            if current:
                gaps.append(_finalize_gap(current, state))
            current = {
                "title": line[4:].strip(),
                "status": "open",
                "priority": "medium",
                "target": "",
                "mode": "append_under_heading",
                "heading": "",
                "aufgabe": "",
                "kriterien": [],
                "suchbegriffe": [],
                "bevorzugte_quellen": [],
                "faktenmuster": [],
                "akzeptanzkriterien": [],
            }
            state = _new_state()
            continue

        if current is None:
            continue

        if line.strip() == "---":
            continue

        stripped = line.strip()

        if stripped == "Aufgabe:":
            state["current_section"] = "aufgabe"
            continue
        if stripped == "Suchbegriffe:":
            state["current_section"] = "suchbegriffe"
            continue
        if stripped == "Bevorzugte Quellen:":
            state["current_section"] = "bevorzugte_quellen"
            continue
        if stripped == "Faktenmuster:":
            state["current_section"] = "faktenmuster"
            continue
        if stripped == "Akzeptanzkriterien:":
            state["current_section"] = "akzeptanzkriterien"
            continue

        section = state["current_section"]

        if section == "aufgabe":
            state["aufgabe_lines"].append(line)
        elif section == "suchbegriffe":
            state["suchbegriffe_lines"].append(line)
        elif section == "bevorzugte_quellen":
            state["bevorzugte_quellen_lines"].append(line)
        elif section == "faktenmuster":
            state["faktenmuster_lines"].append(line)
        elif section == "akzeptanzkriterien":
            state["akzeptanzkriterien_lines"].append(line)
        elif ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"')
            if key in ("status", "priority", "target", "mode", "heading"):
                current[key] = val

    if current:
        gaps.append(_finalize_gap(current, state))

    return gaps


if __name__ == "__main__":
    for gap in load_gaps():
        ak = gap.get("akzeptanzkriterien", [])
        kr = gap.get("kriterien", [])
        sb = gap.get("suchbegriffe", [])
        bq = gap.get("bevorzugte_quellen", [])
        print(f"[{gap['priority']}] {gap['title']} -> {gap['target']}")
        print(f"  Akzeptanzkriterien (strukturiert): {len(ak)}, Legacy: {len(kr)}")
        print(f"  Suchbegriffe: {len(sb)}, Bevorzugte Quellen: {len(bq)}")
        for c in ak:
            print(f"    - type={c.get('type')} required={c.get('required')} {list(c.keys())}")
        print()
