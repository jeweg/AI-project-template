#!/usr/bin/env python3
"""Compose portable agent instruction files from numbered rule fragments.

The numbered fragments in `_agent-rules/` are the editable source. This script
generates `AGENTS.md` for Codex-compatible tools and `CLAUDE.md` as a Claude
Code projection. It is intentionally dependency-free so adopters can run it in
fresh project checkouts.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


SOURCE_DIR = Path(__file__).resolve().parent
ROOT = SOURCE_DIR.parent
AGENTS_PATH = ROOT / "AGENTS.md"
CLAUDE_PATH = ROOT / "CLAUDE.md"
HASH_PATH = SOURCE_DIR / ".agents-md.hash"

GENERATED_HEADER = """# Agent Rules

This file is generated. Direct edits are refused by the next
regenerate to avoid losing them. When the user asks for a rule change,
edit `_agent-rules/*.md` and run `python _agent-rules/compose.py`.
"""

STALE_OUTPUT = 1
USAGE_ERROR = 2
FRAGMENT_ERROR = 3
EDITED_OUTPUT = 4

LOCAL_RULES_NAME = "90-local.md"
IGNORED_FRAGMENT_NAMES = {
    "changelog.md",
    "contributing.md",
    "license.md",
    "notes.md",
    "readme.md",
    "todo.md",
}
FRAGMENT_NAME_RE = re.compile(r"^(\d+)-[\w-]+\.md$", re.IGNORECASE)
FENCE_OPEN_RE = re.compile(r"^\s*(`{3,}|~{3,})")

HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
HEADING_RE = re.compile(r"^( {0,3})(#{1,6})(\s+.*)$")


class FragmentError(Exception):
    """Raised when source fragments cannot be composed safely."""


def usage() -> str:
    return (
        "usage: python _agent-rules/compose.py "
        "[--check] [--include-local] [--force]"
    )


def parse_args(argv: list[str]) -> tuple[bool, bool, bool, bool] | None:
    check = False
    include_local = False
    force = False
    help_requested = False
    for arg in argv:
        if arg == "--check":
            check = True
        elif arg == "--include-local":
            include_local = True
        elif arg == "--force":
            force = True
        elif arg in {"-h", "--help"}:
            help_requested = True
        else:
            print(usage())
            return None
    return check, include_local, force, help_requested


def fragment_sort_key(path: Path) -> tuple[int, str]:
    match = FRAGMENT_NAME_RE.match(path.name)
    if match is None:
        raise FragmentError(
            f"{path.relative_to(ROOT)}: fragment names must match "
            "`<number>-<name>.md`, for example `20-project.md`; "
            "use `*.example.md` for ignored examples"
        )
    return int(match.group(1)), path.name.lower()


def ensure_no_case_duplicates(paths: list[Path]) -> None:
    seen: dict[str, Path] = {}
    for path in paths:
        key = path.name.lower()
        if key in seen:
            first = seen[key].relative_to(ROOT)
            second = path.relative_to(ROOT)
            raise FragmentError(
                f"duplicate fragment names differing only by case: "
                f"{first}, {second}"
            )
        seen[key] = path


def ensure_no_numeric_slot_aliases(paths: list[Path]) -> None:
    seen: dict[tuple[int, str], Path] = {}
    for path in paths:
        match = FRAGMENT_NAME_RE.match(path.name)
        if match is None:
            continue
        prefix = int(match.group(1))
        suffix = path.name[match.end(1):].lower()
        key = (prefix, suffix)
        if key in seen:
            first = seen[key].relative_to(ROOT)
            second = path.relative_to(ROOT)
            raise FragmentError(
                f"duplicate numeric fragment slot: {first}, {second}; "
                "use one spelling for each numbered fragment"
            )
        seen[key] = path


def fragment_files(include_local: bool = False) -> list[Path]:
    paths: list[Path] = []
    if not SOURCE_DIR.is_dir():
        raise FragmentError(f"{SOURCE_DIR.relative_to(ROOT)}: directory missing")
    for path in SOURCE_DIR.iterdir():
        lower_name = path.name.lower()
        if not path.is_file() or not lower_name.endswith(".md"):
            continue
        if lower_name.endswith(".example.md"):
            continue
        if lower_name in IGNORED_FRAGMENT_NAMES:
            continue
        if lower_name == LOCAL_RULES_NAME and not include_local:
            continue
        paths.append(path)
    ensure_no_case_duplicates(paths)
    ensure_no_numeric_slot_aliases(paths)
    return sorted(paths, key=fragment_sort_key)


def visible_content(text: str) -> str:
    return HTML_COMMENT_RE.sub("", text).strip()


def structural_heading_depths(text: str) -> list[int]:
    depths: list[int] = []
    fence_char: str | None = None
    fence_len = 0
    in_html_comment = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if in_html_comment:
            if "-->" in line:
                in_html_comment = False
            continue
        if stripped.startswith("<!--"):
            if "-->" not in stripped:
                in_html_comment = True
            continue
        if fence_char is None:
            fence_match = FENCE_OPEN_RE.match(line)
            if fence_match is not None:
                fence = fence_match.group(1)
                fence_char = fence[0]
                fence_len = len(fence)
                continue
            heading_match = HEADING_RE.match(line)
            if heading_match is not None:
                depths.append(len(heading_match.group(2)))
            continue
        if stripped.startswith(fence_char * fence_len):
            closing_run = len(stripped) - len(stripped.lstrip(fence_char))
            if closing_run >= fence_len:
                fence_char = None
                fence_len = 0
    return depths


def normalize_heading_depth(text: str) -> str:
    """Shift the fragment so its shallowest heading becomes ``##``.

    Fragments are written as standalone Markdown documents; their top-most
    heading might be ``#``, ``##``, or anything else. Take the shallowest
    structural heading in the file (skipping fenced code and HTML comments)
    and shift every heading by the same amount so that level becomes ``##``,
    preserving relative depths. The shallowest heading is not necessarily the
    first one encountered.
    """
    depths = structural_heading_depths(HTML_COMMENT_RE.sub("", text))
    if not depths:
        return text
    shift = 2 - min(depths)
    if shift == 0:
        return text
    if any(depth + shift < 1 or depth + shift > 6 for depth in depths):
        raise FragmentError(
            "cannot normalize fragment heading depths without exceeding "
            "Markdown heading levels"
        )

    out_lines: list[str] = []
    fence_char: str | None = None
    fence_len = 0
    in_html_comment = False
    for line in text.splitlines():
        stripped = line.lstrip()
        if in_html_comment:
            out_lines.append(line)
            if "-->" in line:
                in_html_comment = False
            continue
        if stripped.startswith("<!--"):
            out_lines.append(line)
            if "-->" not in stripped:
                in_html_comment = True
            continue
        if fence_char is None:
            fence_match = FENCE_OPEN_RE.match(line)
            if fence_match is not None:
                fence = fence_match.group(1)
                fence_char = fence[0]
                fence_len = len(fence)
                out_lines.append(line)
                continue
            heading_match = HEADING_RE.match(line)
            if heading_match is not None:
                indent, hashes, rest = heading_match.groups()
                out_lines.append(f"{indent}{'#' * (len(hashes) + shift)}{rest}")
                continue
            out_lines.append(line)
            continue
        out_lines.append(line)
        if stripped.startswith(fence_char * fence_len):
            closing_run = len(stripped) - len(stripped.lstrip(fence_char))
            if closing_run >= fence_len:
                fence_char = None
                fence_len = 0
    return "\n".join(out_lines)


def read_fragment(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8").strip()
    if not visible_content(text):
        return None
    try:
        return normalize_heading_depth(text)
    except FragmentError as exc:
        raise FragmentError(f"{path.relative_to(ROOT)}: {exc}") from exc


def _compose(include_local: bool = False) -> tuple[str, int]:
    parts = [GENERATED_HEADER.rstrip()]
    fragment_count = 0
    for path in fragment_files(include_local=include_local):
        fragment = read_fragment(path)
        if fragment is None:
            continue
        fragment_count += 1
        parts.append(fragment)
    if fragment_count == 0:
        raise FragmentError("_agent-rules/: no composable rule fragments found")
    return "\n\n".join(parts).rstrip() + "\n", fragment_count


def compose_agents(include_local: bool = False) -> str:
    text, _ = _compose(include_local=include_local)
    return text


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stored_hash() -> str | None:
    if not HASH_PATH.exists():
        return None
    content = HASH_PATH.read_text(encoding="utf-8").strip()
    return content or None


EXPECTED_CLAUDE = "@AGENTS.md\n"


def _maybe_write(path: Path, content: str) -> None:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8", newline="\n")


def write_outputs(agents_text: str) -> None:
    _maybe_write(CLAUDE_PATH, EXPECTED_CLAUDE)
    _maybe_write(AGENTS_PATH, agents_text)
    _maybe_write(HASH_PATH, hash_text(agents_text) + "\n")


def edited_warning(files: list[str]) -> str:
    listing = ", ".join(files)
    have = "has" if len(files) == 1 else "have"
    return (
        f"{listing} {have} changes that the composer did not write.\n"
        "Refusing to overwrite to avoid losing manual changes.\n"
        "\n"
        "If the changes belong in agent rules, copy them into\n"
        "`_agent-rules/*.md` and re-run.\n"
        "\n"
        "To overwrite anyway:\n"
        "  python _agent-rules/compose.py --force"
    )


def detect_edits(agents_text: str) -> list[str]:
    edited: list[str] = []
    if AGENTS_PATH.exists():
        current = AGENTS_PATH.read_text(encoding="utf-8")
        if current != agents_text:
            prev = stored_hash()
            if prev is None or hash_text(current) != prev:
                edited.append("AGENTS.md")
    if CLAUDE_PATH.exists():
        current_claude = CLAUDE_PATH.read_text(encoding="utf-8")
        if current_claude != EXPECTED_CLAUDE:
            edited.append("CLAUDE.md")
    return edited


def announce_write(
    fragment_count: int, force: bool, include_local: bool
) -> None:
    flags = []
    if include_local:
        flags.append("--include-local")
    if force:
        flags.append("--force")
    suffix = "" if not flags else ", " + ", ".join(flags)
    noun = "fragment" if fragment_count == 1 else "fragments"
    print(
        f"wrote AGENTS.md and CLAUDE.md ({fragment_count} {noun}{suffix})"
    )


def regenerate(
    agents_text: str,
    fragment_count: int,
    force: bool = False,
    include_local: bool = False,
) -> int:
    if not force:
        edits = detect_edits(agents_text)
        if edits:
            print(edited_warning(edits), file=sys.stderr)
            return EDITED_OUTPUT

    will_change = (
        not AGENTS_PATH.exists()
        or AGENTS_PATH.read_text(encoding="utf-8") != agents_text
        or not CLAUDE_PATH.exists()
        or CLAUDE_PATH.read_text(encoding="utf-8") != EXPECTED_CLAUDE
    )
    write_outputs(agents_text)
    if will_change:
        announce_write(fragment_count, force, include_local)
    return 0


def check_outputs(agents_text: str, local_agents_text: str | None = None) -> int:
    expected_claude = EXPECTED_CLAUDE
    stale: list[str] = []
    current_agents = (
        AGENTS_PATH.read_text(encoding="utf-8")
        if AGENTS_PATH.exists()
        else None
    )
    if current_agents != agents_text:
        stale.append(str(AGENTS_PATH.relative_to(ROOT)))
    if not CLAUDE_PATH.exists() or CLAUDE_PATH.read_text(encoding="utf-8") != expected_claude:
        stale.append(str(CLAUDE_PATH.relative_to(ROOT)))
    if stale:
        stale_without_agents = [
            path for path in stale if path != str(AGENTS_PATH.relative_to(ROOT))
        ]
        if (
            local_agents_text is not None
            and current_agents is not None
            and current_agents == local_agents_text
        ):
            print(
                "AGENTS.md was composed with --include-local; do not commit "
                "local rules. Regenerate without --include-local before "
                "sharing."
            )
            if stale_without_agents:
                print("stale generated file(s): " + ", ".join(stale_without_agents))
                print("run: python _agent-rules/compose.py")
            return STALE_OUTPUT
        print("stale generated file(s): " + ", ".join(stale))
        print("run: python _agent-rules/compose.py")
        return STALE_OUTPUT
    return 0


def main(argv: list[str]) -> int:
    parsed = parse_args(argv)
    if parsed is None:
        return USAGE_ERROR
    check, include_local, force, help_requested = parsed
    if help_requested:
        print(usage())
        return 0
    try:
        agents_text, fragment_count = _compose(include_local=include_local)
    except FragmentError as exc:
        print(exc, file=sys.stderr)
        return FRAGMENT_ERROR
    local_agents_text = None
    if check and not include_local:
        try:
            local_agents_text = compose_agents(include_local=True)
        except FragmentError:
            local_agents_text = None
    if check:
        return check_outputs(agents_text, local_agents_text=local_agents_text)
    return regenerate(
        agents_text,
        fragment_count=fragment_count,
        force=force,
        include_local=include_local,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
