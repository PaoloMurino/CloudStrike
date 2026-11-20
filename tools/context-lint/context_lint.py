#!/usr/bin/env python3
"""CloudStrike Context Linter.

Validates the Context Engineering artifacts (steering, specs, skills, hooks) for
format and cross-reference consistency. Standard library only (no dependencies),
so it can run from any hook on any machine.

Phase 0 scope (implemented now): steering format + rule-ID uniqueness, broken
`#[[file:]]` references, and the `always`-steering line budget.
Later phases fill in: requirements (EARS/IDs), traceability (REQ<->task), skills.

Usage:
    python3 context_lint.py all           # run every available check
    python3 context_lint.py steering      # steering files only
    python3 context_lint.py requirements  # spec requirements (phase 2)
    python3 context_lint.py traceability  # REQ<->task coverage (phase 2/4)
    python3 context_lint.py skill         # skills (phase 3)

Exit code 0 = clean, 1 = findings. Designed to be called by .kiro/hooks.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Repo root = two levels up from this file (tools/context-lint/).
ROOT = Path(__file__).resolve().parents[2]
KIRO = ROOT / ".kiro"
STEERING = KIRO / "steering"

# Rule-ID namespaces owned by steering (see context-governance.md).
_NS = r"(?:SEC|ARC|AG|MC|QA|SPEC|PROV-AWS|PROV-AZ|PROV-GCP)-\d{2}"
# A definition leads a bullet with a bold ID, e.g. "- **SEC-05 ...**". References
# (e.g. "(`SEC-05`)") are not definitions and must not count as duplicates.
RULE_DEF_RE = re.compile(rf"(?:^|\n)\s*[-*]?\s*\*\*({_NS})\b")
FILE_REF_RE = re.compile(r"#\[\[file:([^\]]+)\]\]")
VALID_INCLUSION = {"always", "fileMatch", "manual", "auto"}

# Budget: keep the always-loaded steering lean so it fits every prompt.
ALWAYS_LINE_BUDGET = 900


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def merge(self, other: "Report") -> None:
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

    def print_and_exit(self) -> None:
        for w in self.warnings:
            print(f"warning: {w}")
        for e in self.errors:
            print(f"error: {e}")
        if self.errors:
            print(f"\ncontext-lint: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
            sys.exit(1)
        print(f"context-lint: clean ({len(self.warnings)} warning(s))")
        sys.exit(0)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Return (frontmatter dict, body). Frontmatter must start at line 1."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4 :]
    fm: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm, body


def check_steering(report: Report) -> None:
    if not STEERING.is_dir():
        report.error(f"steering directory not found: {STEERING}")
        return

    seen_ids: dict[str, str] = {}
    for md in sorted(STEERING.glob("*.md")):
        rel = md.relative_to(ROOT)
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)

        # Frontmatter + inclusion mode.
        if not fm:
            report.error(f"{rel}: missing frontmatter (must start at line 1)")
        inclusion = fm.get("inclusion", "always")
        if inclusion not in VALID_INCLUSION:
            report.error(f"{rel}: invalid inclusion '{inclusion}'")
        if inclusion == "fileMatch" and "fileMatchPattern" not in fm:
            report.error(f"{rel}: inclusion fileMatch requires fileMatchPattern")
        if inclusion == "auto" and not ("name" in fm and "description" in fm):
            report.error(f"{rel}: inclusion auto requires name and description")

        # Rule-ID uniqueness across all steering files (definitions only).
        for m in RULE_DEF_RE.finditer(body):
            rid = m.group(1)
            if rid in seen_ids:
                where = seen_ids[rid]
                if where == str(rel):
                    report.error(f"{rid} defined more than once in {rel}")
                else:
                    report.error(f"{rid} defined in both {where} and {rel}")
            else:
                seen_ids[rid] = str(rel)

        # Broken file references.
        for m in FILE_REF_RE.finditer(text):
            target = (ROOT / m.group(1)).resolve()
            if not target.exists():
                report.error(f"{rel}: broken file reference #[[file:{m.group(1)}]]")

        # Line budget for always-loaded steering.
        if inclusion == "always":
            n = len(text.splitlines())
            if n > ALWAYS_LINE_BUDGET:
                report.warn(f"{rel}: {n} lines of always-steering (soft budget {ALWAYS_LINE_BUDGET})")

    if seen_ids:
        print(f"context-lint: {len(seen_ids)} steering rule IDs across {len(set(seen_ids.values()))} files")


def check_requirements(report: Report) -> None:
    # Phase 2: parse .kiro/specs/*/requirements.md for REQ IDs + EARS criteria.
    specs = KIRO / "specs"
    if not specs.is_dir():
        print("context-lint: no specs yet (requirements check skipped)")
        return
    print("context-lint: requirements check not implemented yet (phase 2)")


def check_traceability(report: Report) -> None:
    # Phase 2/4: ensure every REQ is covered by a task and vice versa.
    print("context-lint: traceability check not implemented yet (phase 2)")


def check_skill(report: Report) -> None:
    # Phase 3: validate .kiro/skills/*/SKILL.md frontmatter and references.
    print("context-lint: skill check not implemented yet (phase 3)")


CHECKS = {
    "steering": check_steering,
    "requirements": check_requirements,
    "traceability": check_traceability,
    "skill": check_skill,
}


def main(argv: list[str]) -> None:
    cmd = argv[1] if len(argv) > 1 else "all"
    report = Report()
    if cmd == "all":
        for fn in CHECKS.values():
            fn(report)
    elif cmd in CHECKS:
        CHECKS[cmd](report)
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        print(__doc__)
        sys.exit(2)
    report.print_and_exit()


if __name__ == "__main__":
    main(sys.argv)
