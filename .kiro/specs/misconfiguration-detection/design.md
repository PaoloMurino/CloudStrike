# Misconfiguration Detection — Design

Implements `requirements.md`. Rules cited by ID.

## Modules

- `catalogs/controls/*.yaml` — rule definitions: `id`, `severity`, `match` (graph pattern),
  `finding` template, `remediation_hint`. Data only (`REQ-DETECT-01`, `ARC-03`, `QA-08`).
- `core/rules/engine.py` — evaluates rules against the graph, emits Finding nodes with evidence
  (`REQ-DETECT-02`, `REQ-DETECT-05`).
- `core/rules/baselines.py` — permission baselines for excessive-permission detection
  (`REQ-DETECT-03`).

## Key decisions

- Findings are first-class graph nodes linked via `PROTECTED_BY`/edges to the offending elements, so
  paths and reports reuse them (`MC-04`).
- Risky-trust rules target the `federation`/condition attributes on CAN_ASSUME/TRUSTS edges
  (`REQ-DETECT-04`).
- Deterministic emit: Findings sorted by (severity, canonical id) (`QA-01`).

## Properties to test

- Adding a YAML rule changes output with no engine change.
- Same graph → identical Findings with evidence.
- Known excessive-permission and risky-trust fixtures each raise the expected Finding.
