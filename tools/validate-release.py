#!/usr/bin/env python3
"""Validate HITL·Work documentation references and the distributable .skill archive."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "hitl-work.skill"
DOCS = (ROOT / "SKILL.md", ROOT / "README.md")


def referenced_agent_files() -> set[str]:
    references: set[str] = set()
    for document in DOCS:
        content = document.read_text(encoding="utf-8")
        references.update(re.findall(r"`([a-z0-9-]+\.md)`", content))
    artifacts = {
        "doubt-review.md",
        "prd.md",
        "qa-report.md",
        "skill.md",
        "status.md",
        "task-1.md",
        "task-2.md",
        "task-N.md",
        "test-plan.md",
        "ui-spec.md",
    }
    return {name for name in references if name not in artifacts}


def main() -> int:
    errors: list[str] = []
    agent_files = referenced_agent_files()

    for name in sorted(agent_files):
        if not (ROOT / name).is_file():
            errors.append(f"Referenced agent file is missing from source: {name}")

    if not ARCHIVE.is_file():
        errors.append(f"Release archive is missing: {ARCHIVE.name}")
    else:
        with zipfile.ZipFile(ARCHIVE) as package:
            archived = {Path(name).name for name in package.namelist() if name.endswith(".md")}
        for name in sorted(agent_files):
            if name not in archived:
                errors.append(f"Referenced agent file is missing from archive: {name}")
        if "SKILL.md" not in archived or "README.md" not in archived:
            errors.append("Archive must include SKILL.md and README.md")

    if errors:
        print("Release validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Release validation passed: {len(agent_files)} referenced agent files are present in source and archive.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
