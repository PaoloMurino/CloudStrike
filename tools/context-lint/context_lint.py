#!/usr/bin/env python3
"""CloudStrike Context Linter.

Validates the Context Engineering artifacts (steering, specs, skills, hooks) for
format and cross-reference consistency. Standard library only (no dependencies),
so it can run from any hook on any machine.

Checks implemented:
- steering     : frontmatter, inclusion mode, rule-ID uniqueness, broken file refs, always-budget.
- requirements : unique REQ IDs, EARS ('SHALL') present, governing-rule refs resolve to steering.
- traceability : every REQ covered by a task, every task REQ exists (per spec).
- skill        : SKILL.md frontmatter (name==folder, <=64, description<=1024) + bundled file refs.

Checks run clean when the artifact type does not exist yet, so hooks can be installed early.

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

# Requirement IDs: REQ-<SPEC>-NN, defined as a bold or heading lead, referenced
# elsewhere (e.g. in tasks via "_Requirements: REQ-GRAPH-01_").
REQ_ID_RE = re.compile(r"(REQ-[A-Z]+-\d{2})(?!\d)")
REQ_DEF_RE = re.compile(r"(?:^|\n)(?:#{1,6}\s*|\s*[-*]?\s*\*\*)(REQ-[A-Z]+-\d{2})\b")
ANY_RULE_REF_RE = re.compile(rf"\b({_NS})\b")
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")

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


def collect_steering_ids() -> set[str]:
    """All rule IDs defined across steering files (used for reference checks)."""
    ids: set[str] = set()
    if not STEERING.is_dir():
        return ids
    for md in STEERING.glob("*.md"):
        _, body = parse_frontmatter(md.read_text(encoding="utf-8"))
        for m in RULE_DEF_RE.finditer(body):
            ids.add(m.group(1))
    return ids


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
    """SPEC-02/03/04: unique REQ IDs, EARS criteria, valid governing-rule refs."""
    specs = KIRO / "specs"
    if not specs.is_dir():
        print("context-lint: no specs yet (requirements check skipped)")
        return

    steering_ids = collect_steering_ids()
    defined: dict[str, str] = {}
    count = 0
    for req in sorted(specs.glob("*/requirements.md")):
        rel = req.relative_to(ROOT)
        text = req.read_text(encoding="utf-8")

        # REQ ID uniqueness (definitions only).
        for m in REQ_DEF_RE.finditer(text):
            rid = m.group(1)
            count += 1
            if rid in defined:
                report.error(f"{rid} defined in both {defined[rid]} and {rel}")
            else:
                defined[rid] = str(rel)

        # SPEC-03: EARS form expected somewhere in the file.
        if "SHALL" not in text:
            report.error(f"{rel}: no EARS acceptance criteria (no 'SHALL' found)")

        # SPEC-04: governing rule references must resolve to a real steering ID.
        for m in ANY_RULE_REF_RE.finditer(text):
            if m.group(1) not in steering_ids:
                report.error(f"{rel}: references unknown steering rule {m.group(1)}")

    if defined:
        print(f"context-lint: {len(defined)} requirement IDs across {len(set(defined.values()))} specs")
    else:
        print("context-lint: no requirement IDs found yet")


def check_traceability(report: Report) -> None:
    """SPEC-05: every REQ is covered by a task and every task REQ exists."""
    specs = KIRO / "specs"
    if not specs.is_dir():
        print("context-lint: no specs yet (traceability check skipped)")
        return

    for spec_dir in sorted(p for p in specs.iterdir() if p.is_dir()):
        req_file = spec_dir / "requirements.md"
        task_file = spec_dir / "tasks.md"
        if not req_file.exists():
            continue

        defined = {m.group(1) for m in REQ_DEF_RE.finditer(req_file.read_text(encoding="utf-8"))}
        if not task_file.exists():
            if defined:
                report.error(f"{spec_dir.relative_to(ROOT)}: requirements exist but tasks.md is missing")
            continue

        referenced = set(REQ_ID_RE.findall(task_file.read_text(encoding="utf-8")))
        for rid in sorted(defined - referenced):
            report.error(f"{rid} is defined but not covered by any task in {task_file.relative_to(ROOT)}")
        for rid in sorted(referenced - defined):
            report.error(f"{task_file.relative_to(ROOT)}: task references unknown requirement {rid}")


def check_skill(report: Report) -> None:
    """Skill frontmatter + reference integrity (agentskills.io spec)."""
    skills = KIRO / "skills"
    if not skills.is_dir():
        print("context-lint: no skills yet (skill check skipped)")
        return

    found = 0
    for skill_md in sorted(skills.glob("*/SKILL.md")):
        found += 1
        rel = skill_md.relative_to(ROOT)
        folder = skill_md.parent.name
        fm, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))

        name = fm.get("name", "")
        if not name:
            report.error(f"{rel}: missing 'name' in frontmatter")
        else:
            if name != folder:
                report.error(f"{rel}: name '{name}' must match folder '{folder}'")
            if not SKILL_NAME_RE.match(name):
                report.error(f"{rel}: name '{name}' must be lowercase/digits/hyphens, <=64 chars")

        desc = fm.get("description", "")
        if not desc:
            report.error(f"{rel}: missing 'description' in frontmatter")
        elif len(desc) > 1024:
            report.error(f"{rel}: description is {len(desc)} chars (max 1024)")

        # Referenced bundled files (references/..., scripts/..., assets/...) must exist.
        for m in re.finditer(r"\b((?:references|scripts|assets)/[^\s`)\]]+)", body):
            if not (skill_md.parent / m.group(1)).exists():
                report.error(f"{rel}: broken skill reference '{m.group(1)}'")

    print(f"context-lint: {found} skill(s) checked")


CHECKS = {
    "steering": check_steering,
    "requirements": check_requirements,
    "traceability": check_traceability,
    "skill": check_skill,
}


# Shell commands that would MUTATE a cloud estate (SEC-01). The guard scans the
# raw PreToolUse payload, so it is robust to the exact JSON field names.
MUTATION_RE = re.compile(
    r"\baws\s+[\w-]+\s+(create|put|delete|update|attach|detach|modify|run|terminate|assume-role)"
    r"|\baz\s+[\w-]+\s+(create|delete|update|set|assign)"
    r"|\bgcloud\s+[\w-]+\s+(create|delete|update|set|add-iam-policy-binding)"
    r"|\bterraform\s+(apply|destroy)",
    re.IGNORECASE,
)


def run_guard() -> None:
    """PreToolUse guard: block mutating cloud CLI commands (SEC-01). Exit 2 blocks."""
    payload = sys.stdin.read() if not sys.stdin.isatty() else ""
    m = MUTATION_RE.search(payload)
    if m:
        print(
            "SEC-01: blocked a command that would mutate a cloud estate "
            f"('{m.group(0)}'). Use Simulated mode (digital twin), or a probe with a "
            "declared Authorization Scope (SEC-05).",
            file=sys.stderr,
        )
        sys.exit(2)
    sys.exit(0)


def main(argv: list[str]) -> None:
    cmd = argv[1] if len(argv) > 1 else "all"
    if cmd == "guard":
        run_guard()
        return
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
