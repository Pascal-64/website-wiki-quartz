#!/usr/bin/env python3
"""Build targeted context for a wiki gap — budget-aware, no blind full-file loading."""

import re
from pathlib import Path

CONTENT_DIR = Path("content")
MAX_CONTEXT_CHARS = 20000
STYLE_FILE = Path(__file__).parent / "wiki_style.md"


def load_style_guide() -> str:
    return STYLE_FILE.read_text(encoding="utf-8") if STYLE_FILE.exists() else ""


def get_known_pages() -> list[str]:
    return sorted(
        md.stem
        for md in CONTENT_DIR.rglob("*.md")
        if md.name not in ("index.md", "wiki-gaps.md")
    )


def extract_frontmatter(content: str) -> str:
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[: end + 4]
    return ""


def extract_headings(content: str) -> str:
    return "\n".join(line for line in content.split("\n") if re.match(r"^#+\s", line))


def _heading_level(line: str) -> int:
    m = re.match(r"^(#+)\s", line.strip())
    return len(m.group(1)) if m else 0


def extract_section(content: str, heading: str) -> str:
    """Return the full section content from heading until the next same/higher-level heading."""
    target = heading.strip('"').strip()
    target_level = _heading_level(target)
    lines = content.split("\n")
    section: list[str] = []
    in_section = False

    for line in lines:
        if line.strip() == target:
            in_section = True
            section.append(line)
            continue
        if in_section:
            lvl = _heading_level(line)
            if lvl > 0 and lvl <= target_level:
                break
            section.append(line)

    return "\n".join(section)


def build_context(gap: dict, max_chars: int = MAX_CONTEXT_CHARS) -> dict:
    """Return context dict with budget-aware components (highest priority first)."""
    target_path = Path(gap["target"])
    if not target_path.exists():
        return {
            "task": gap.get("aufgabe", gap.get("title", "")),
            "frontmatter": "",
            "headings": "",
            "target_section": "",
            "known_pages": "",
        }

    file_content = target_path.read_text(encoding="utf-8")

    task = gap.get("aufgabe", gap.get("title", ""))
    frontmatter = extract_frontmatter(file_content)
    headings = extract_headings(file_content)
    target_section = extract_section(file_content, gap.get("heading", ""))
    known_pages = ", ".join(get_known_pages())

    # Priority-based budget trimming
    budget = max_chars - len(task)
    target_section_trimmed = target_section[: min(8000, budget // 2)]
    budget -= len(target_section_trimmed)
    headings_trimmed = headings[:min(2000, budget // 2)]
    budget -= len(headings_trimmed)
    frontmatter_trimmed = frontmatter[:min(500, budget // 2)]
    budget -= len(frontmatter_trimmed)
    known_pages_trimmed = known_pages[:min(2000, budget)]

    return {
        "task": task,
        "style_guide": load_style_guide(),
        "frontmatter": frontmatter_trimmed,
        "headings": headings_trimmed,
        "target_section": target_section_trimmed,
        "known_pages": known_pages_trimmed,
    }
