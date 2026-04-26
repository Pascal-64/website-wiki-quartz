#!/usr/bin/env python3
"""Scans wiki pages, calculates gap scores, updates the auto-report in wiki-gaps.md."""

import re
import sys
import yaml
from pathlib import Path
from datetime import date

CONTENT_DIR = Path("content")
GAPS_FILE = CONTENT_DIR / "wiki-gaps.md"
MIN_GAP_SCORE = 3


def parse_frontmatter(content: str) -> tuple[dict, str]:
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}, content
    try:
        fm = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, content[match.end():]


def gap_score(filepath: Path, content: str) -> int:
    fm, body = parse_frontmatter(content)
    score = 0

    word_count = len(body.split())
    if word_count < 250:
        score += 2

    if fm.get("status") == "draft":
        score += 2

    if re.search(r"\bTODO:", content):
        score += 2

    if "## Quellenbasis" not in content and "## Quellen" not in content:
        score += 1

    if not re.findall(r"\[\[.+?\]\]", body):
        score += 1

    if "```" not in content:
        score += 1

    if not re.search(r"## (Relevanz|Warum|Bedeutung|Einordnung)", content):
        score += 1

    return score


def update_report(rows: list[tuple[str, int, int]]) -> None:
    if not GAPS_FILE.exists():
        print("wiki-gaps.md not found, skipping report update.")
        return

    content = GAPS_FILE.read_text(encoding="utf-8")
    today = date.today().isoformat()

    if rows:
        table = (
            f"_Zuletzt analysiert: {today}_\n\n"
            "| Seite | Gap-Score | Wörter |\n"
            "|-------|-----------|--------|\n"
        )
        for page, score, words in rows:
            table += f"| {page} | {score} | {words} |\n"
    else:
        table = f"_Zuletzt analysiert: {today}_\n\n_Keine Lücken mit Score ≥ {MIN_GAP_SCORE} gefunden._\n"

    # Replace or append the auto-report section
    section_header = "## Automatisch erkannte Lücken (Report – nur lesen, nicht auto-schreiben)"
    if section_header in content:
        content = re.sub(
            rf"({re.escape(section_header)}\n).*",
            lambda m: m.group(1) + table,
            content,
            flags=re.DOTALL,
        )
    else:
        content = content.rstrip() + f"\n\n{section_header}\n{table}"

    GAPS_FILE.write_text(content, encoding="utf-8")
    print(f"Report updated: {len(rows)} pages with gap score >= {MIN_GAP_SCORE}")


def main() -> None:
    skip_names = {"index.md", "wiki-gaps.md"}
    scored: list[tuple[str, int, int]] = []

    for md_file in sorted(CONTENT_DIR.rglob("*.md")):
        if md_file.name in skip_names:
            continue
        try:
            content = md_file.read_text(encoding="utf-8")
            score = gap_score(md_file, content)
            _, body = parse_frontmatter(content)
            words = len(body.split())
            if score >= MIN_GAP_SCORE:
                rel = str(md_file.relative_to(CONTENT_DIR))
                scored.append((rel, score, words))
                print(f"Gap: {rel}  score={score}  words={words}")
        except Exception as exc:
            print(f"Error processing {md_file}: {exc}", file=sys.stderr)

    scored.sort(key=lambda x: x[1], reverse=True)
    update_report(scored)


if __name__ == "__main__":
    main()
