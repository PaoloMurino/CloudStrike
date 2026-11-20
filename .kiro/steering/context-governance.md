---
inclusion: manual
---

# CloudStrike — Context Governance

How the Context Engineering system itself is organized and changed. Pull this in with
`#context-governance` when editing the context (steering, specs, skills, hooks). It defines the ID
scheme every artifact uses and the rules that keep the four pillars non-overlapping.

## The four pillars and their single responsibility

| Pillar | Owns | Must not contain |
| --- | --- | --- |
| **Steering** (`.kiro/steering`) | Permanent MUST/MUST NOT rules with stable IDs; the glossary | Feature requirements; procedures |
| **Specs** (`.kiro/specs`) | Verifiable per-feature behavior (EARS), design, tasks | Global rules (cite them by ID) |
| **Skills** (`.kiro/skills`) | Reusable domain know-how: how to do a thing, checklists, templates | Rules; feature requirements |
| **Hooks** (`.kiro/hooks`) | Automated enforcement, thin, delegating to `context-lint` | Duplicated rule logic |

## ID namespaces (single source per namespace)

- Steering rules: `SEC-*` (security/authorization), `ARC-*` (architecture/boundaries),
  `AG-*` (agentic), `MC-*` (canonical model), `QA-*` (quality/process), `SPEC-*` (spec authoring),
  `PROV-AWS-*` / `PROV-AZ-*` / `PROV-GCP-*` (provider specifics).
- Architecture decisions: `AD-*` (recorded in this file's companion decision log / README).
- Requirements: `REQ-<SPEC>-NN`.

An ID is defined in exactly one place and referenced everywhere else. Never restate a rule's text
under a different pillar.

## Architecture decisions (AD) index

`AD-01` canonical graph · `AD-02` ports & adapters · `AD-03` read-only ingestion ·
`AD-04` deterministic simulation · `AD-05` data-driven technique catalog · `AD-06` cross-cloud trust ·
`AD-07` remediation = graph patch · `AD-08` explicit scoring · `AD-09` approved stack ·
`AD-10` sensitive-data handling · `AD-11` agentic architecture · `AD-12` deploy-anywhere probes ·
`AD-13` native CSP APIs · `AD-14` authorization & scope model · `AD-15` Simulated + Live modes.

## Changing the context

- **Add a rule:** choose the right namespace, give it the next free number, put it only in its
  steering file, then reference it from specs/skills/hooks as needed.
- **Retire a rule:** mark it deprecated in place with a pointer to its replacement; never reuse the ID.
- **Add a spec/skill/hook:** follow `spec-authoring.md` / the skill template / the hook catalog, and
  make sure `context-lint` passes.

## Consistency gates

Every change is validated by `tools/context-lint` (format, orphan/duplicate IDs, requirement↔task
coverage, broken `#[[file:]]` references, stray global rules inside specs) and, at phase boundaries,
by the `context-consistency-audit` skill for semantic review. Behavioral tests in
`context-eval/behavioral-tests.md` confirm the context drives the intended agent behavior.
