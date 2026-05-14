#!/usr/bin/env python3
"""Verify the knowledge layer's mechanically-checkable invariants.

Reports findings on stdout, one per line, and does NOT modify any
file. Exits 0 if clean, 1 if findings, 2 on fundamental error
(no `_knowledge/` directory found).

Scope is deliberately limited to the rules `AGENTS.md` calls
"not optional" and that are deterministically checkable from file
content alone. Things that require meaning -- whether the hot
list reflects current priorities, whether OVERVIEW.md describes the
namespace shape correctly, whether freshness markers are honest --
are agent responsibilities, not script responsibilities, and stay
out of scope.

Recovery from accidental deletion is also out of scope: the script
reports missing files with a hint to restore them from git or from
the template repo, and leaves the recovery itself to the user. Git
already handles the case for any project with the pre-shipped files
committed; the script does not duplicate the defaults to handle
the rarer case where they are not.

Running this in the pristine template repo itself reports the two
pre-shipped files (`STATE.md` and `materials/OVERVIEW.md`) as
unbootstrapped because their sentinel banners are still present.
That is the expected output for the template, not a bug; the script
is intended for adopter projects after bootstrap.

Checks performed:

* Bootstrap state of pre-shipped knowledge files
  (`_knowledge/STATE.md` and `_knowledge/materials/OVERVIEW.md`):
  flags if the sentinel banner is still present (unbootstrapped),
  or, if the banner is gone, flags any remaining `<...>` placeholder
  text or literal `YYYY-MM-DD` markers (broken bootstrap), with the
  line numbers where they occur. Missing files are flagged with a
  recovery hint. Code blocks are excluded from the placeholder scan
  so language generics like `Map<String, Integer>` do not trip it.
* `INDEX.md` membership: every working file in `_knowledge/materials/`
  has a `## <filename>` entry, and every entry points at a file that
  exists. Only `## <filename>.md` headings are treated as entries, so
  notes and preambles in `INDEX.md` are not mistaken for stale
  entries. Reports missing entries, stale entries, duplicate entries,
  and any subdirectories under `materials/` (the namespace is flat).

Run from any directory inside the project; the script walks up to
find the `_knowledge/` directory.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


BANNER_PHRASE = "template default content"

PRE_SHIPPED_WITH_BANNER = (
    "_knowledge/STATE.md",
    "_knowledge/materials/OVERVIEW.md",
)

INDEX_PATH = "_knowledge/materials/INDEX.md"
MATERIALS_DIR = "_knowledge/materials"
CANONICAL_MATERIALS_FILES = frozenset({"INDEX.md", "OVERVIEW.md"})

# Match `<...>` placeholders containing whitespace. Every template
# skeleton placeholder contains at least one space, so the whitespace
# requirement is sufficient and single-token prose forms like `<name>`
# or `<thing>` are not flagged. Brackets containing `=` or `"` are
# excluded so HTML attributes like `<img src="x" alt="y">` and similar
# tag-shaped content do not trip the check. Code blocks (fenced and
# inline) are blanked out before this regex runs, so language generics
# like `Map<String, Integer>` inside code samples do not match either;
# see `_strip_code_for_placeholder_check`.
PLACEHOLDER_RE = re.compile(r'<[^<>="]*\s[^<>="]*>')
DATE_PLACEHOLDER_RE = re.compile(r"\bYYYY-MM-DD\b")
# Index entries name a markdown filename: `## foo.md` or
# `## 2026-05-14-handoff.md`. Other `##` headings (preambles, notes,
# meta sections) are not treated as entries. The character class
# matches the descriptive lowercase filenames the template recommends
# plus any case the agent might use; the trailing `.md` is required.
INDEX_HEADING_RE = re.compile(r"^##\s+([\w.\-]+\.md)\s*$")

def recovery_hint(rel_path: str) -> str:
    return (
        f"restore with `git checkout HEAD -- {rel_path}` or copy "
        f"from the template repo"
    )


def find_project_root(start: Path) -> Path | None:
    """Walk up from `start` looking for a directory containing `_knowledge/`."""
    for ancestor in [start.resolve()] + list(start.resolve().parents):
        if (ancestor / "_knowledge").is_dir():
            return ancestor
    return None


def first_non_empty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line
    return ""


def _strip_code_for_placeholder_check(text: str) -> str:
    """Blank out fenced code blocks and inline-code spans so they do not
    trigger placeholder false positives, while preserving line numbers
    so finding locations match the original file."""
    out_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out_lines.append("")
            continue
        if in_fence:
            out_lines.append("")
            continue
        out_lines.append(re.sub(r"`[^`]*`", "", line))
    return "\n".join(out_lines)


def _line_number(text: str, offset: int) -> int:
    """1-based line number of `offset` in `text`."""
    return text.count("\n", 0, offset) + 1


def _format_locations(line_numbers: list[int]) -> str:
    if len(line_numbers) == 1:
        return f"at line {line_numbers[0]}"
    return "at lines " + ", ".join(str(n) for n in line_numbers)


def check_bootstrap(root: Path) -> list[str]:
    findings: list[str] = []
    for rel in PRE_SHIPPED_WITH_BANNER:
        path = root / rel
        if not path.is_file():
            findings.append(
                f"{rel}: missing (template-shipped, expected to be "
                f"present); {recovery_hint(rel)}"
            )
            continue
        text = path.read_text(encoding="utf-8")
        first = first_non_empty_line(text)
        banner_present = first.startswith(">") and BANNER_PHRASE in text[:1000]
        if banner_present:
            findings.append(
                f"{rel}: sentinel banner still present (unbootstrapped); "
                f"use provided context or ask the user, fill the file, "
                f"remove the banner"
            )
            continue
        scrubbed = _strip_code_for_placeholder_check(text)
        placeholder_lines = sorted(
            {_line_number(scrubbed, m.start()) for m in PLACEHOLDER_RE.finditer(scrubbed)}
        )
        date_lines = sorted(
            {_line_number(text, m.start()) for m in DATE_PLACEHOLDER_RE.finditer(text)}
        )
        if placeholder_lines or date_lines:
            parts: list[str] = []
            if placeholder_lines:
                parts.append(
                    f"{len(placeholder_lines)} `<...>` placeholder(s) "
                    f"{_format_locations(placeholder_lines)}"
                )
            if date_lines:
                parts.append(
                    f"{len(date_lines)} unfilled `YYYY-MM-DD` marker(s) "
                    f"{_format_locations(date_lines)}"
                )
            findings.append(
                f"{rel}: banner gone but " + " and ".join(parts)
                + " remain (broken bootstrap); finish replacing the defaults"
            )
    return findings


def parse_index_entries(text: str) -> list[str]:
    """Return filenames named in `## <filename>.md` headings of INDEX.md.

    Only headings whose text matches a markdown filename are returned.
    Other `##` sections (preambles, meta notes, etc.) are ignored, so
    `INDEX.md` may freely contain non-entry sections without polluting
    the membership check.
    """
    entries: list[str] = []
    for line in text.splitlines():
        m = INDEX_HEADING_RE.match(line)
        if m:
            entries.append(m.group(1))
    return entries


def list_working_files(materials_dir: Path) -> list[str]:
    """List .md files in `materials/`, excluding canonical artifacts.

    Subdirectories are not returned; they are out of contract for
    `materials/` and are reported separately by `check_index_membership`.
    """
    return sorted(
        p.name
        for p in materials_dir.iterdir()
        if p.is_file()
        and p.suffix == ".md"
        and p.name not in CANONICAL_MATERIALS_FILES
    )


def list_materials_subdirs(materials_dir: Path) -> list[str]:
    """List subdirectory names directly under `materials/`."""
    return sorted(
        p.name
        for p in materials_dir.iterdir()
        if p.is_dir()
    )


def check_index_membership(root: Path) -> list[str]:
    findings: list[str] = []
    materials_dir = root / MATERIALS_DIR
    index_path = root / INDEX_PATH
    if not materials_dir.is_dir():
        findings.append(
            f"{MATERIALS_DIR}: directory missing; "
            f"{recovery_hint(INDEX_PATH)}"
        )
        return findings
    for subdir in list_materials_subdirs(materials_dir):
        findings.append(
            f"{MATERIALS_DIR}/{subdir}/: subdirectory under materials/ "
            f"(materials/ is a flat namespace; flatten the file or move "
            f"it to _knowledge/archive/)"
        )
    if not index_path.is_file():
        findings.append(
            f"{INDEX_PATH}: missing; {recovery_hint(INDEX_PATH)}"
        )
        return findings
    working_files = set(list_working_files(materials_dir))
    raw_entries = parse_index_entries(index_path.read_text(encoding="utf-8"))
    seen: dict[str, int] = {}
    for name in raw_entries:
        seen[name] = seen.get(name, 0) + 1
    duplicates = sorted(name for name, count in seen.items() if count > 1)
    for name in duplicates:
        findings.append(
            f"{INDEX_PATH}: entry for `{name}` appears {seen[name]} times "
            f"(duplicate; keep one entry)"
        )
    index_entries = set(raw_entries)
    missing = sorted(working_files - index_entries)
    stale = sorted(index_entries - working_files)
    for name in missing:
        findings.append(
            f"{MATERIALS_DIR}/{name}: present but not listed in INDEX.md "
            f"(add an entry)"
        )
    for name in stale:
        findings.append(
            f"{INDEX_PATH}: entry for `{name}` but file no longer present "
            f"in materials/ (remove or update the entry)"
        )
    return findings


def main() -> int:
    root = find_project_root(Path.cwd())
    if root is None:
        print(
            "error: no `_knowledge/` directory found in current path or any "
            "ancestor",
            file=sys.stderr,
        )
        return 2

    findings: list[str] = []
    findings.extend(check_bootstrap(root))
    findings.extend(check_index_membership(root))

    if not findings:
        print("clean")
        return 0
    for f in findings:
        print(f)
    return 1


if __name__ == "__main__":
    sys.exit(main())
