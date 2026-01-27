#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys


BEGIN_MARKER = "<!-- BEGIN CONTROLLEDREDUCTION EXAMPLES -->"
END_MARKER = "<!-- END CONTROLLEDREDUCTION EXAMPLES -->"


def extract_examples_block(pyx_path: Path) -> str:
    text = pyx_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    try:
        start_idx = next(i for i, line in enumerate(lines) if "Examples::" in line) + 1
    except StopIteration as exc:
        raise ValueError("Could not find 'Examples::' block in docstring") from exc

    block: list[str] = []
    i = start_idx
    while i < len(lines):
        line = lines[i]
        if line.strip() == "":
            block.append("")
            i += 1
            continue
        if line.startswith("    "):
            block.append(line[4:])
            i += 1
            continue
        break

    while block and block[-1] == "":
        block.pop()

    if not block:
        raise ValueError("Examples block is empty")
    return "\n".join(block)


def replace_readme_block(readme_path: Path, block: str, check: bool) -> int:
    text = readme_path.read_text(encoding="utf-8")
    if BEGIN_MARKER not in text or END_MARKER not in text:
        raise ValueError("README markers not found")

    before, rest = text.split(BEGIN_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)

    snippet = "```\n" + block + "\n```\n"
    replacement = BEGIN_MARKER + "\n" + snippet + END_MARKER
    new_text = before + replacement + after

    if new_text == text:
        return 0

    if check:
        sys.stderr.write("README examples are out of date. Run tools/update_readme_examples.py\n")
        return 1

    readme_path.write_text(new_text, encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync README examples from controlledreduction.pyx")
    parser.add_argument("--check", action="store_true", help="fail if README is out of date")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    pyx_path = root / "pycontrolledreduction" / "controlledreduction.pyx"
    readme_path = root / "README.md"

    block = extract_examples_block(pyx_path)
    return replace_readme_block(readme_path, block, args.check)


if __name__ == "__main__":
    raise SystemExit(main())
