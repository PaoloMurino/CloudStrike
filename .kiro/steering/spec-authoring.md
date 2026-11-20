---
inclusion: fileMatch
fileMatchPattern: [".kiro/specs/**"]
---

# CloudStrike — Spec Authoring Standard

Rules (`SPEC-*`) for writing specs. Loaded whenever a spec file is touched. Keeps specs verifiable and
traceable to steering rules. Terms follow `product.md`.

## Structure

- **SPEC-01 Three files.** Each feature spec is `.kiro/specs/<feature>/` with `requirements.md`,
  `design.md`, `tasks.md`. Requirements-First order.
- **SPEC-02 Requirement IDs.** Every requirement has a stable ID `REQ-<SPEC>-NN`, where `<SPEC>` is the
  spec's short code (GRAPH, DETECT, PATHS, SIM, REMED, VIZ, ORCH, PROBE). IDs are never renumbered;
  deprecated ones are marked, not reused.
- **SPEC-03 EARS acceptance criteria.** Each requirement lists acceptance criteria in EARS form:
  `WHEN <condition/event> THE SYSTEM SHALL <behavior>`. Criteria MUST be verifiable (observable output
  or state), not aspirational.

## Traceability

- **SPEC-04 Cite governing rules.** `requirements.md` opens with a "Governing rules" section listing
  the steering rule IDs the spec implements (e.g. `SEC-05`, `MC-03`). Reference by ID; do not restate
  the rule text (anti-duplication).
- **SPEC-05 Tasks link to requirements.** Every task in `tasks.md` ends with `_Requirements: REQ-...,
  REQ-..._`. Every `REQ-*` MUST be covered by at least one task; no task without a requirement.
- **SPEC-06 Design references, not rules.** `design.md` explains how the requirements are met and may
  cite steering rules by ID, but never redefines a global rule or a glossary term.

## Content discipline

- **SPEC-07 No global rules in specs.** A spec states feature behavior only. Permanent MUST/SHALL
  rules that apply platform-wide belong in steering; a spec references them.
- **SPEC-08 Security-sensitive specs cite SEC.** Any spec touching Live mode, probes, credentials or
  mutation MUST cite the relevant `SEC-*` rules in its Governing rules section and encode them as EARS
  criteria.
