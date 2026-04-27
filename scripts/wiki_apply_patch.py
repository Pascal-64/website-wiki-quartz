#!/usr/bin/env python3
"""Apply a generated markdown patch to a target content file."""

import re
from pathlib import Path


def _heading_level(line: str) -> int:
    m = re.match(r"^(#+)\s", line.strip())
    return len(m.group(1)) if m else 0


def apply_patch(file_content: str, patch: str, heading: str, mode: str) -> str | None:
    """
    Apply patch to file_content and return the updated content.
    Returns None if the heading is not found (for heading-dependent modes).

    Modes:
      append_under_heading  — inserts before the next same/higher-level heading
      insert_after_heading  — inserts immediately after the heading line
      append_to_file        — appends at the end of the file
    """
    patch_text = patch.strip()

    if mode == "append_to_file":
        return file_content.rstrip() + "\n\n" + patch_text + "\n"

    if mode in ("append_under_heading", "insert_after_heading"):
        target = heading.strip('"').strip()
        target_level = _heading_level(target)
        lines = file_content.split("\n")

        found_idx = None
        for i, line in enumerate(lines):
            if line.strip() == target:
                found_idx = i
                break

        if found_idx is None:
            return None

        if mode == "insert_after_heading":
            insert_pos = found_idx + 1
        else:
            # append_under_heading: find the end of this section
            insert_pos = len(lines)
            for i in range(found_idx + 1, len(lines)):
                lvl = _heading_level(lines[i])
                if lvl > 0 and lvl <= target_level:
                    insert_pos = i
                    break

        new_lines = (
            lines[:insert_pos]
            + [""]
            + patch_text.split("\n")
            + [""]
            + lines[insert_pos:]
        )
        return "\n".join(new_lines)

    return None


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5:
        print("Usage: wiki_apply_patch.py <target_file> <patch_file> <heading> <mode>")
        sys.exit(1)
    target = Path(sys.argv[1])
    patch_file = Path(sys.argv[2])
    hdg = sys.argv[3]
    md = sys.argv[4]
    result = apply_patch(target.read_text(encoding="utf-8"), patch_file.read_text(encoding="utf-8"), hdg, md)
    if result is None:
        print(f"Error: heading not found: {hdg!r}", file=sys.stderr)
        sys.exit(1)
    target.write_text(result, encoding="utf-8")
    print(f"Patch applied to {target}")
