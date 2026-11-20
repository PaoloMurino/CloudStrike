# Attack Path Analysis — Design

Implements `requirements.md`. Rules cited by ID.

## Modules

- `catalogs/techniques/*.yaml` — one technique per file: `id`, `attack` (MITRE id), `preconditions`
  (graph pattern), `effect` (edge/state added). Data only (`REQ-PATHS-01`, `ARC-03`).
- `core/paths/catalog.py` — load + schema-validate techniques; reject invalid (`REQ-PATHS-02`).
- `core/paths/matcher.py` — match preconditions against the graph, returning bindings + evidence
  (`REQ-PATHS-03`).
- `core/paths/engine.py` — forward search composing applicable techniques into paths, including
  cross-provider chaining via CAN_ASSUME/TRUSTS (`REQ-PATHS-04`); deterministic frontier ordering
  (`REQ-PATHS-06`).
- `core/paths/scoring.py` — the formula in `requirements.md` (`REQ-PATHS-05`).

## Key decisions

- Techniques are pure data; the engine is generic (`QA-08`). A technique's `effect` adds a virtual
  edge, enabling later techniques — this is how chains form.
- Determinism: the search frontier is a sorted queue keyed by (risk desc, path length, canonical id);
  no reliance on dict/set order (`QA-01`).
- Analysis is read-only over the graph (`REQ-PATHS-07`, `SEC-02`); it never calls an adapter's action
  path.

## Properties to test

- Adding a YAML technique changes results with zero engine code change (`REQ-PATHS-01`).
- Same graph+catalog → identical ordered paths (`REQ-PATHS-06`).
- A cross-cloud fixture yields one composed path spanning two providers (`REQ-PATHS-04`).
- Every returned path carries score factors and per-step evidence (`REQ-PATHS-05`).
