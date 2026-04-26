#!/usr/bin/env python3
"""Validates JSON patches from fill_wiki_gaps.py and applies them to wiki files."""

import json
import re
import sys
import yaml
from pathlib import Path
from datetime import date

CONTENT_DIR = Path("content")
PATCHES_DIR = Path("tmp/wiki-patches")
APPLIED_DIR = Path("tmp/wiki-patches-applied")
LOG_FILE = Path("tmp/validation-log.json")

BANNED_PHRASES = [
    "Als KI", "Als Sprachmodell", "Ich bin eine KI",
    "als KI", "als Sprachmodell", "Als großes Sprachmodell",
]


def validate(patch: dict) -> tuple[bool, list[str], list[str]]:
    errors, warnings = [], []

    for field in ("patch_markdown", "sources", "confidence"):
        if field not in patch:
            errors.append(f"Missing field: {field}")

    if errors:
        return False, errors, warnings

    if not patch["sources"]:
        errors.append("sources list is empty")

    text = patch.get("patch_markdown", "")
    for phrase in BANNED_PHRASES:
        if phrase in text:
            errors.append(f"Banned phrase: '{phrase}'")

    if not text.strip():
        errors.append("patch_markdown is empty")

    if len(text) > 12000:
        errors.append(f"patch_markdown too long ({len(text)} chars, max 12000)")

    if patch.get("confidence", 1) < 0.7:
        warnings.append(f"Low confidence: {patch['confidence']}")

    if not patch.get("target_file"):
        warnings.append("No target_file — patch cannot be applied automatically")

    # Validate wikilinks reference existing files
    wiki_stems = {f.stem.lower() for f in CONTENT_DIR.rglob("*.md")}
    for link in re.findall(r"\[\[([^\]|]+)", text):
        stem = link.split("/")[-1].lower().replace(" ", "-")
        if stem not in wiki_stems:
            warnings.append(f"Wikilink may not exist: [[{link}]]")

    return len(errors) == 0, errors, warnings


def apply(patch: dict, target: Path) -> bool:
    text = patch["patch_markdown"]
    today = date.today().isoformat()

    if target.exists():
        existing = target.read_text(encoding="utf-8")

        # Safety: refuse if patch is > 80% of existing length
        if len(text) > len(existing) * 0.8:
            print(f"  SAFETY: patch ({len(text)} chars) > 80% of existing ({len(existing)} chars), skipping")
            return False

        insert_after = patch.get("insert_after_heading", "")
        if insert_after and insert_after in existing:
            new_content = existing.replace(insert_after, insert_after + "\n\n" + text, 1)
        elif "## Quellenbasis" in existing:
            new_content = existing.replace("## Quellenbasis", text + "\n\n## Quellenbasis", 1)
        elif "## Siehe auch" in existing:
            new_content = existing.replace("## Siehe auch", text + "\n\n## Siehe auch", 1)
        else:
            new_content = existing.rstrip() + "\n\n" + text + "\n"

        # Update frontmatter date
        new_content = re.sub(
            r"(zuletzt_aktualisiert:\s*)[\d-]+",
            f"zuletzt_aktualisiert: {today}",
            new_content,
        )
    else:
        title = patch.get("_gap_item", {}).get("title", target.stem).split("–")[0].strip()
        sources_block = "\n".join(f"- {s}" for s in patch.get("sources", []))
        new_content = (
            f"---\ntitle: {title}\nstatus: draft\ntyp: thema\n"
            f"zuletzt_aktualisiert: {today}\n---\n\n# {title}\n\n"
            f"{text}\n\n## Quellenbasis\n{sources_block}\n"
        )
        target.parent.mkdir(parents=True, exist_ok=True)

    target.write_text(new_content, encoding="utf-8")
    return True


def main() -> None:
    if not PATCHES_DIR.exists() or not list(PATCHES_DIR.glob("*.json")):
        print("No patches to validate.")
        sys.exit(0)

    APPLIED_DIR.mkdir(parents=True, exist_ok=True)
    Path("tmp").mkdir(exist_ok=True)

    log = []
    applied_count = 0

    for patch_file in sorted(PATCHES_DIR.glob("*.json")):
        print(f"\nValidating: {patch_file.name}")
        try:
            patch = json.loads(patch_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"  Invalid JSON: {exc}", file=sys.stderr)
            log.append({"file": str(patch_file), "status": "json_error", "errors": [str(exc)]})
            continue

        ok, errors, warnings = validate(patch)
        entry = {
            "file": patch_file.name,
            "topic": patch.get("_gap_item", {}).get("title", "?"),
            "target": patch.get("target_file"),
            "confidence": patch.get("confidence"),
            "errors": errors,
            "warnings": warnings,
            "status": "valid" if ok else "invalid",
        }

        for e in errors:
            print(f"  ERROR: {e}", file=sys.stderr)
        for w in warnings:
            print(f"  WARN:  {w}")

        if not ok:
            log.append(entry)
            continue

        target_path = Path(patch["target_file"].replace("\\", "/")) if patch.get("target_file") else None
        if not target_path:
            entry["status"] = "no_target"
            log.append(entry)
            continue

        success = apply(patch, target_path)
        entry["status"] = "applied" if success else "apply_failed"
        if success:
            applied_count += 1
            print(f"  Applied → {target_path}")
            (APPLIED_DIR / patch_file.name).write_text(
                patch_file.read_text(encoding="utf-8"), encoding="utf-8"
            )
            patch_file.unlink()
        else:
            print(f"  Apply failed for: {target_path}", file=sys.stderr)

        log.append(entry)

    LOG_FILE.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nApplied: {applied_count} patch(es). Log: {LOG_FILE}")
    sys.exit(0)


if __name__ == "__main__":
    main()
