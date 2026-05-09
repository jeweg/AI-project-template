#!/usr/bin/env python3
"""Opt in to LF-only line endings for a derived project.

Stdlib-only on purpose: this script should run on baseline Python 3
across Windows, macOS, and Linux.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


GITATTRIBUTES = """\
* text=auto eol=lf

*.gif binary
*.gz binary
*.ico binary
*.jpeg binary
*.jpg binary
*.pdf binary
*.png binary
*.webp binary
"""

EDITORCONFIG = """\
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
"""


def run_git(args: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def in_git_repo() -> bool:
    try:
        return run_git(["rev-parse", "--is-inside-work-tree"]).returncode == 0
    except OSError:
        return False


def repo_root() -> Path:
    if not in_git_repo():
        return Path.cwd()
    proc = run_git(["rev-parse", "--show-toplevel"], check=True)
    return Path(proc.stdout.strip())


def git_config_value(key: str) -> str | None:
    proc = run_git(["config", "--get", key])
    value = proc.stdout.strip()
    return value or None


def git_config_with_origin(key: str) -> str | None:
    proc = run_git(["config", "--show-origin", "--get", key])
    value = proc.stdout.strip()
    return value or None


def warn_git_config() -> None:
    if not in_git_repo():
        print("Git config: not in a Git repo; skipping introspection.")
        return

    autocrlf = git_config_value("core.autocrlf")
    eol = git_config_value("core.eol")

    print("Git line-ending config:")
    for key in ("core.autocrlf", "core.eol", "core.safecrlf"):
        print(f"  {key}: {git_config_with_origin(key) or '<unset>'}")

    if autocrlf == "true":
        print(
            "WARNING: core.autocrlf=true may write CRLF working-tree files "
            "in repos without .gitattributes.",
            file=sys.stderr,
        )
    if eol == "crlf":
        print(
            "WARNING: core.eol=crlf conflicts with an LF-only repo policy.",
            file=sys.stderr,
        )


def tracked_files() -> list[Path]:
    proc = run_git(["ls-files"], check=True)
    return [Path(line) for line in proc.stdout.splitlines() if line]


def is_binary(data: bytes) -> bool:
    return b"\0" in data


def crlf_files() -> list[Path]:
    found: list[Path] = []
    for path in tracked_files():
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if is_binary(data):
            continue
        if b"\r\n" in data or b"\r" in data:
            found.append(path)
    return found


def normalize_tracked_text() -> list[Path]:
    changed: list[Path] = []
    for path in tracked_files():
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if is_binary(data):
            continue
        normalized = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if normalized != data:
            path.write_bytes(normalized)
            changed.append(path)
    return changed


def write_policy_files() -> None:
    Path(".gitattributes").write_text(GITATTRIBUTES, encoding="utf-8", newline="\n")
    Path(".editorconfig").write_text(EDITORCONFIG, encoding="utf-8", newline="\n")


def dirty_status() -> str:
    if not in_git_repo():
        return ""
    proc = run_git(["status", "--short"], check=True)
    return proc.stdout.strip()


def print_crlf_inventory() -> None:
    found = crlf_files()
    for path in found:
        print(path.as_posix())
    print(f"CRLF_FILES={len(found)}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Opt in to LF-only line endings for this repository.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="report what would happen without writing files",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="commit the mechanical LF policy change if the repo is clean",
    )
    args = parser.parse_args()

    root = repo_root()
    # Keep paths simple and make the script independent of where it is called from.
    import os

    os.chdir(root)

    warn_git_config()

    if args.dry_run:
        print()
        print("Would write .gitattributes and .editorconfig.")
        if in_git_repo():
            print()
            print("Current tracked CRLF inventory:")
            print_crlf_inventory()
        return 0

    if in_git_repo() and dirty_status():
        print(
            "Refusing to apply LF policy with a dirty working tree.\n"
            "Commit, stash, or discard existing changes first.",
            file=sys.stderr,
        )
        return 1

    write_policy_files()

    if in_git_repo():
        print()
        print("Normalizing tracked text files:")
        changed = normalize_tracked_text()
        for path in changed:
            print(path.as_posix())
        print(f"NORMALIZED={len(changed)}")

        print()
        print("Post-normalization CRLF scan:")
        print_crlf_inventory()

        check = run_git(["diff", "--check"])
        if check.stdout:
            print(check.stdout, end="")
        if check.stderr:
            print(check.stderr, end="", file=sys.stderr)
        if check.returncode != 0:
            return check.returncode

        if args.commit:
            run_git(["add", ".gitattributes", ".editorconfig"], check=True)
            names = run_git(["diff", "--name-only", "-z"], check=True).stdout
            if names:
                subprocess.run(
                    ["git", "add", "--pathspec-from-file=-", "--pathspec-file-nul"],
                    input=names,
                    text=True,
                    check=True,
                )
            run_git(["commit", "-m", "chore: normalize text files to LF"], check=True)
        else:
            print()
            print("Review with: git status --short && git diff --stat")
            print("Commit separately when satisfied.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
