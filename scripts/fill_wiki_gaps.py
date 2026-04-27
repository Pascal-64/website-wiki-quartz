#!/usr/bin/env python3
"""Reads open gaps from wiki-gaps.md, calls Claude + web search, writes JSON patches."""

import json
import os
import re
import sys
import time
from pathlib import Path
from datetime import date

import anthropic

CONTENT_DIR = Path("content")
GAPS_FILE = CONTENT_DIR / "wiki-gaps.md"
PATCHES_DIR = Path("tmp/wiki-patches")
MAX_GAPS_PER_RUN = int(os.getenv("MAX_GAPS_PER_RUN", "2"))
MAX_TOKENS = 2500
SLEEP_SECONDS = int(os.getenv("CLAUDE_SLEEP_SECONDS", "65"))

SYSTEM_PROMPT = """Du erweiterst ein deutsches Technik-Wiki im Obsidian/Quartz-Format.

Regeln:
- Erweitere nur das angegebene Thema. Erhalte bestehenden Inhalt vollständig.
- Schreibe sachlich, technisch, klar. Keine Marketing-Sprache.
- Keine erfundenen Quellen. Jede faktische Aussage braucht eine Quelle.
- Nutze Wikilinks [[Thema]] nur wenn sie sinnvoll sind und die Seite im Wiki existiert.
- Erzeuge keinen kompletten Artikel neu, sondern einen ergänzenden Abschnitt (Patch).
- Keine "Als KI"- oder "Als Sprachmodell"-Formulierungen. Schreibe auf Deutsch.

Gib NUR valides JSON zurück, ohne Markdown-Code-Block darum:
{
  "summary": "Kurze Beschreibung was ergänzt wurde",
  "target_file": "content/Themen/LLM.md",
  "patch_markdown": "## Neuer Abschnitt\\n\\nInhalt...",
  "insert_after_heading": "## Kernkonzepte",
  "sources": ["https://...", "https://..."],
  "internal_links": ["[[Transformer]]"],
  "confidence": 0.85,
  "needs_human_review": false
}"""


def parse_json_response(text: str) -> dict:
    text = text.strip()
    text = re.sub(r"^```json?\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in Claude response: {text[:200]}")
    return json.loads(match.group(0))


def parse_open_items(content: str) -> list[dict]:
    items = []
    lines = content.split("\n")
    in_manual = False
    current: dict | None = None

    for line in lines:
        if line.startswith("## Manuell eingetragen"):
            in_manual = True
            continue
        if line.startswith("## ") and in_manual:
            in_manual = False
            if current:
                items.append(current)
                current = None
            continue
        if not in_manual:
            continue

        if line.startswith("- [ ]"):
            if current:
                items.append(current)
            current = {"raw_line": line, "title": line[5:].strip(), "status": "open", "priority": "medium"}
        elif current and re.match(r"\s+status:", line):
            current["status"] = line.split(":", 1)[1].strip()
        elif current and re.match(r"\s+priority:", line):
            current["priority"] = line.split(":", 1)[1].strip()
        elif line.startswith("- ["):
            if current:
                items.append(current)
            current = None

    if current:
        items.append(current)

    return [i for i in items if i["status"] == "open"]


def find_sources(content: str) -> list[str]:
    sources, in_section = [], False
    for line in content.split("\n"):
        if line.startswith("## Quellen"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.strip().startswith("- http"):
            sources.append(line.strip()[2:].strip())
    return sources


def find_target_file(title: str) -> Path | None:
    topic = title.split("–")[0].strip().lower().replace(" ", "-")
    for md in CONTENT_DIR.rglob("*.md"):
        if md.name in ("index.md", "wiki-gaps.md"):
            continue
        if topic in md.stem.lower() or md.stem.lower() in topic:
            return md
    return None


def call_claude(item: dict, existing: str, extra_sources: list[str]) -> dict | None:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    source_block = ""
    if extra_sources:
        sources_text = "\n".join(f"- {s}" for s in extra_sources)[:8000]
        source_block = "\n\nBereits vorhandene Quellen zum Thema:\n" + sources_text

    existing_block = ""
    if existing:
        existing_block = f"\n\nBestehender Inhalt der Seite (NICHT überschreiben oder neu schreiben):\n```\n{existing[:2500]}\n```"

    user_msg = (
        f"Thema: {item['title']}"
        f"{source_block}"
        f"{existing_block}"
        "\n\nBitte recherchiere und erstelle den ergänzenden Abschnitt. "
        "Gib NUR das JSON zurück, keinen Markdown-Code-Block."
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        messages=[{"role": "user", "content": user_msg}],
    )

    text = "".join(b.text for b in response.content if b.type == "text")
    if not text.strip():
        print(f"  No text in response for: {item['title']}")
        return None

    try:
        return parse_json_response(text)
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"  JSON parse error: {exc}\n  Response: {text[:300]}", file=sys.stderr)
        return None


def main() -> None:
    if not GAPS_FILE.exists():
        print(f"wiki-gaps.md not found at {GAPS_FILE}")
        sys.exit(0)

    content = GAPS_FILE.read_text(encoding="utf-8")
    open_items = parse_open_items(content)
    if not open_items:
        print("No open gaps. Nothing to do.")
        sys.exit(0)

    prio = {"high": 0, "medium": 1, "low": 2}
    open_items.sort(key=lambda x: prio.get(x["priority"], 1))
    to_process = open_items[:MAX_GAPS_PER_RUN]

    extra_sources = find_sources(content)
    PATCHES_DIR.mkdir(parents=True, exist_ok=True)
    written = 0

    for item in to_process:
        print(f"\nProcessing: {item['title']}")
        target = find_target_file(item["title"])
        existing = target.read_text(encoding="utf-8") if target and target.exists() else ""
        print(f"  Target: {target}")

        patch = call_claude(item, existing, extra_sources)
        if patch is None:
            print("  Skipped: no valid patch generated.")
            continue

        if not patch.get("target_file") and target:
            patch["target_file"] = str(target).replace("\\", "/")

        patch["_gap_item"] = item

        slug = re.sub(r"[^\w]", "_", item["title"][:50])

        patch_path = PATCHES_DIR / f"{slug}.json"
        patch_path.write_text(json.dumps(patch, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  Patch written: {patch_path.name}")
        written += 1

        if written < len(to_process):
            print(f"  Sleeping {SLEEP_SECONDS}s to avoid rate limit...")
            time.sleep(SLEEP_SECONDS)

        # Mark item as pending review in wiki-gaps.md
        updated = content.replace(
            f"  status: open\n  priority: {item['priority']}",
            f"  status: review\n  priority: {item['priority']}\n  last_attempt: {date.today().isoformat()}\n  pr: pending",
        )
        if updated != content:
            GAPS_FILE.write_text(updated, encoding="utf-8")
            content = updated

    print(f"\n{written} patch(es) written.")
    sys.exit(0)


if __name__ == "__main__":
    main()
