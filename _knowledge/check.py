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
  text or literal `YYYY-MM-DD` markers (broken bootstrap). Missing
  files are flagged with a recovery hint.
* `INDEX.md` membership: every working file in `_knowledge/materials/`
  has a `## <filename>` entry, and every entry points at a file
  that exists. Reports missing entries and stale entries.

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

# Match `<...>` placeholders containing whitespace, including
# placeholders that span multiple lines (newlines allowed inside
# the brackets). Every template skeleton placeholder contains at
# least one space, so the whitespace requirement is sufficient and
# prose forms like `<name>` or `<thing>` (single-token, no
# whitespace) are not false-positive flagged. Nested `<...<...>...>`
# is rejected because `[^<>]` excludes inner brackets. The skeleton
# is deliberately authored without single-token placeholders so
# this regex does not need any special cases.
PLACEHOLDER_RE = re.compile(r"<[^<>]*\s[^<>]*>")
DATE_PLACEHOLDER_RE = re.compile(r"\bYYYY-MM-DD\b")
INDEX_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")

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


def check_bootstrap(root: Path) -> list[str]:
    findings: list[str] = []
    for rel in PRE_SHIPPED_WITH_BANNER:
        path = root / rel
        if not path.exists():
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
                f"interview the user, fill the file, remove the banner"
            )
            continue
        placeholders = PLACEHOLDER_RE.findall(text)
        unfilled_dates = DATE_PLACEHOLDER_RE.findall(text)
        if placeholders or unfilled_dates:
            parts: list[str] = []
            if placeholders:
                parts.append(f"{len(placeholders)} `<...>` placeholder(s)")
            if unfilled_dates:
                parts.append(
                    f"{len(unfilled_dates)} unfilled `YYYY-MM-DD` marker(s)"
                )
            findings.append(
                f"{rel}: banner gone but " + " and ".join(parts)
                + " remain (broken bootstrap); finish replacing the defaults"
            )
    return findings


def parse_index_entries(text: str) -> list[str]:
    """Return filenames named in `## <filename>` headings of INDEX.md."""
    entries: list[str] = []
    for line in text.splitlines():
        m = INDEX_HEADING_RE.match(line)
        if m:
            entries.append(m.group(1))
    return entries


def list_working_files(materials_dir: Path) -> list[str]:
    """List lowercase .md files in `materials/`, excluding canonical artifacts."""
    return sorted(
        p.name
        for p in materials_dir.iterdir()
        if p.is_file()
        and p.suffix == ".md"
        and p.name not in CANONICAL_MATERIALS_FILES
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
    if not index_path.exists():
        findings.append(
            f"{INDEX_PATH}: missing; {recovery_hint(INDEX_PATH)}"
        )
        return findings
    working_files = set(list_working_files(materials_dir))
    index_entries = set(
        parse_index_entries(index_path.read_text(encoding="utf-8"))
    )
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
