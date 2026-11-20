---
name: context-consistency-audit
description: Use when editing the CloudStrike context (steering, specs, skills, hooks) or at a phase boundary, to verify the four pillars stay consistent and non-duplicated. Runs the context-lint tool and performs the semantic review a script cannot.
---

# Context Consistency Audit

Meta-skill that keeps the Context Engineering system coherent. Pairs with `context-governance.md` and
the `tools/context-lint/` validator.

## When to use
- After adding or changing any steering rule, spec, skill or hook.
- At the end of each build phase before moving on.
- Before the demo, as a final gate.

## Automated pass (run first)
Run the validator and resolve every error:
```
python3 tools/context-lint/context_lint.py all
```
It checks steering format and rule-ID uniqueness, requirement IDs and EARS, requirement↔task
traceability, broken `#[[file:]]` references, and skill frontmatter.

## Semantic pass (what the script cannot see)
1. **No duplication.** A rule's substance appears in exactly one pillar; specs/skills/hooks reference
   it by ID. Flag any restated rule text.
2. **No contradiction.** A spec or skill never weakens a `SEC-*`/`ARC-*`/`AG-*` rule. Security-
   sensitive specs cite the relevant `SEC-*` (`SPEC-08`).
3. **Completeness.** Every `SEC-*` rule is backed by at least one hook or a behavioral test. Every
   capability in `product.md` has a spec. Every skill has a clear activation trigger.
4. **Glossary discipline.** Terms match `product.md`; no synonyms introduced.
5. **Traceability closure.** Steering rule → REQ → design → task → hook is unbroken for the slice
   under review.

## Output
A short report: automated result, semantic findings, and the exact fix per finding (which file, which
ID). Do not fix silently; record what changed so the chain stays auditable.

## Boundaries
This skill audits the context. It does not implement product features or relax a guardrail to make a
check pass.
