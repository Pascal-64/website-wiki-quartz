#!/usr/bin/env python3
"""Validate generated markdown before applying to content/."""

import re
from pathlib import Path

CONTENT_DIR = Path("content")

FLOSKELN = [
    "hier ist", "gerne", "natürlich", "basierend auf", "ich erstelle",
    "ich werde", "hier sind", "selbstverständlich", "certainly", "sure",
]


def _normalize_link(name: str) -> str:
    return re.sub(r"[-_\s]+", "-", name).lower()


def check_structured_criteria(generated: str, gap: dict, sources_text: str = "") -> list[str]:
    """Check structured akzeptanzkriterien. Returns unmet criteria as warning strings."""
    unmet: list[str] = []
    for c in gap.get("akzeptanzkriterien", []):
        ctype = c.get("type", "")
        label = f"[{ctype}]"

        if ctype == "table":
            has_table = "|---|" in generated or "| ---" in generated
            if not has_table:
                unmet.append(f"Kriterium {label}: Keine Markdown-Tabelle gefunden.")
            else:
                missing = [t for t in c.get("contains", []) if t.lower() not in generated.lower()]
                if missing:
                    unmet.append(f"Kriterium {label}: Tabelle fehlt Einträge: {missing}")

        elif ctype == "code":
            lang = c.get("language", "")
            pattern = f"```{lang}" if lang else "```"
            if pattern not in generated:
                unmet.append(f"Kriterium {label}: Kein {pattern}-Codeblock gefunden.")
            else:
                missing = [t for t in c.get("contains", []) if t.lower() not in generated.lower()]
                if missing:
                    unmet.append(f"Kriterium {label}: Codeblock fehlt Begriffe: {missing}")

        elif ctype == "contains_all":
            missing = [t for t in c.get("terms", []) if t.lower() not in generated.lower()]
            if missing:
                unmet.append(f"Kriterium {label}: Fehlende Begriffe: {missing}")

        elif ctype == "contains_any":
            terms = c.get("terms", [])
            if terms and not any(t.lower() in generated.lower() for t in terms):
                unmet.append(f"Kriterium {label}: Keiner dieser Begriffe gefunden: {terms}")

        elif ctype == "sources":
            min_q = c.get("min", 1)
            count = sources_text.count("### Quelle")
            if count < min_q:
                unmet.append(f"Kriterium {label}: Nur {count} Quellen, min. {min_q} erwartet.")

        elif ctype == "forbidden_terms":
            found = [t for t in c.get("terms", []) if t.lower() in generated.lower()]
            if found:
                unmet.append(f"Kriterium {label}: Verbotene Begriffe gefunden: {found}")

    return unmet


def check_criteria(generated: str, gap: dict, sources_text: str = "") -> list[str]:
    """Legacy check for free-text kriterien. Returns unmet criteria as warning strings."""
    unmet: list[str] = []
    for k in gap.get("kriterien", []):
        kl = k.lower()
        if "tabelle" in kl or "table" in kl:
            if "|---|" not in generated and "| ---" not in generated:
                unmet.append(f"Kriterium nicht erfüllt: {k}")
        elif "codebeispiel" in kl or ("code" in kl and "peft" in kl):
            if "```python" not in generated:
                unmet.append(f"Kriterium nicht erfüllt: {k}")
        elif "qlora" in kl and any(w in kl for w in ("speicher", "consumer", "hardware")):
            if not re.search(r"90\s*%|consumer.{0,20}hardware|speicher\w*reduz", generated, re.I):
                unmet.append(f"Kriterium nicht erfüllt: {k}")
        elif "dpo" in kl and "reward" in kl:
            if not re.search(r"reward.{0,10}model|belohnungsmodell", generated, re.I):
                unmet.append(f"Kriterium nicht erfüllt: {k}")
        elif "quellen" in kl:
            m = re.search(r"(\d+)", kl)
            min_q = int(m.group(1)) if m else 1
            count = sources_text.count("### Quelle")
            if count < min_q:
                unmet.append(f"Kriterium nicht erfüllt: {k} (hat {count})")
    return unmet


def validate(generated: str, gap: dict, sources_text: str = "") -> tuple[list[str], list[str]]:
    """Returns (errors, warnings). Non-empty errors block patch application."""
    errors: list[str] = []
    warnings: list[str] = []

    text = generated.strip()

    if not text:
        errors.append("Ausgabe ist leer.")
        return errors, warnings

    if len(text) < 100:
        errors.append(f"Ausgabe zu kurz ({len(text)} Zeichen, min. 100).")

    first_line = text.split("\n")[0].strip()

    if not re.match(r"^#{2,}\s", first_line):
        errors.append(f"Beginnt nicht mit einer Markdown-Überschrift: {first_line[:80]!r}")
    else:
        heading = gap.get("heading", "").strip('"').strip()
        if heading:
            m = re.match(r"^(#+)\s", heading)
            if m:
                target_level = len(m.group(1))
                expected_prefix = "#" * (target_level + 1) + " "
                if not first_line.startswith(expected_prefix):
                    errors.append(
                        f"Heading-Ebene falsch: erwartet '{expected_prefix.strip()}', "
                        f"gefunden: {first_line[:60]!r}"
                    )

    lower_start = text[:80].lower()
    for floskel in FLOSKELN:
        if lower_start.startswith(floskel):
            errors.append(f"Beginnt mit Modellfloskel: {first_line[:80]!r}")
            break

    if re.match(r"^```", text) and text.rstrip().endswith("```"):
        errors.append("Ausgabe komplett in Markdown-Codeblock eingewickelt.")

    if re.search(r"^\s*\{", text, re.MULTILINE) and re.search(r'"\w+":', text):
        errors.append("Ausgabe enthält JSON statt Markdown.")

    if re.search(r"<html|<body|<div\s|<p>", text, re.IGNORECASE):
        errors.append("Ausgabe enthält HTML als Hauptformat.")

    if "[[]]" in text:
        errors.append("Leere Wikilinks [[]] gefunden.")

    if re.search(r"\\\(|\\\)|\\\[|\\\]", text):
        errors.append(r"LaTeX-Notation \(...\) gefunden — bitte $...$ verwenden (Quartz).")

    target_path = Path(gap.get("target", ""))
    if not target_path.exists():
        errors.append(f"Zieldatei existiert nicht: {gap.get('target')}")
    else:
        file_content = target_path.read_text(encoding="utf-8")
        heading = gap.get("heading", "").strip('"').strip()
        if heading and heading not in file_content:
            errors.append(f"Ziel-Heading nicht gefunden in Datei: {heading!r}")

        gen_headings = [h.strip() for h in re.findall(r"^#{2,}\s+(.+)$", text, re.MULTILINE)]
        file_headings = [h.strip() for h in re.findall(r"^#{2,}\s+(.+)$", file_content, re.MULTILINE)]
        for h in gen_headings:
            if h in file_headings:
                errors.append(f"Überschrift existiert bereits in Zieldatei: {h!r}")

    # Criteria check: structured if available, else legacy
    if gap.get("akzeptanzkriterien"):
        unmet = check_structured_criteria(text, gap, sources_text)
    else:
        unmet = check_criteria(text, gap, sources_text)
    warnings.extend(unmet)

    # General warnings
    wikilinks = re.findall(r"\[\[([^\]]+)\]\]", text)
    if wikilinks:
        known_normalized = {
            _normalize_link(md.stem)
            for md in CONTENT_DIR.rglob("*.md")
            if md.name not in ("index.md", "wiki-gaps.md")
        }
        for link in wikilinks:
            page = link.split("|")[0].strip()
            if _normalize_link(page) not in known_normalized:
                warnings.append(f"Unbekannter Wikilink: [[{page}]]")
    else:
        warnings.append("Keine internen Wikilinks.")

    if len(text) > 8000:
        warnings.append(f"Sehr langer Abschnitt ({len(text)} Zeichen).")

    if "http" not in text and "quelle" not in text.lower() and "source" not in text.lower():
        warnings.append("Keine Quellen/Referenzen angegeben.")

    return errors, warnings


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: wiki_validate.py <generated.md> <gap_target> [gap_heading]")
        sys.exit(1)
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    gap = {"target": sys.argv[2], "heading": sys.argv[3] if len(sys.argv) > 3 else ""}
    errs, warns = validate(text, gap)
    for e in errs:
        print(f"ERROR: {e}")
    for w in warns:
        print(f"WARN:  {w}")
    sys.exit(1 if errs else 0)
