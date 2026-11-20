---
name: attack-path-analysis
description: Use when authoring attack techniques, defining graph edges for attacker movement, or implementing the path-composition and scoring algorithm. Explains the technique schema (preconditions to effect), how techniques chain across clouds, and the explicit risk-scoring model.
---

# Attack Path Analysis

How CloudStrike turns a graph into ranked, explainable attack paths. Pairs with the `PATHS` spec.
Know-how only; the scoring formula is owned by the PATHS spec and cited here.

## When to use
- Adding a technique to `catalogs/techniques/`.
- Implementing or reviewing the path engine or scoring.
- Building a cross-cloud movement scenario.

## Technique schema (data, not code — `QA-08`)
Each technique is one YAML file with:
- `id` and `attack` (MITRE ATT&CK Cloud id).
- `preconditions`: a graph pattern (node/edge shape + attribute conditions) that must match.
- `effect`: the edge or state it produces (e.g. a new CAN_ASSUME, or control of a Principal).
A technique missing any of these is rejected (`REQ-PATHS-02`).

## How chains form
The engine applies a technique where preconditions match, adds its `effect` as a virtual edge, then
re-evaluates — enabling later techniques. Cross-cloud chaining happens naturally when an `effect`
produces a CAN_ASSUME/TRUSTS edge into another provider (`REQ-PATHS-04`, `MC-03`).

## Authoring guidance
- Keep preconditions minimal and attribute-driven so a technique is provider-neutral where possible.
- Put provider specifics in `aws.*`/`azure.*`/`gcp.*` attribute conditions, not in engine logic.
- Always cite the matched evidence so the path is explainable (`QA-03`).

## Scoring (reference)
Risk = likelihood × impact per the formula in the PATHS spec (`REQ-PATHS-05`). Attach the factors
(precondition certainty, enforcing controls on the step, target blast radius) to the path.

## Determinism
Composition and ranking must be reproducible for the same graph+catalog (`REQ-PATHS-06`, `QA-01`):
sort the frontier by (risk desc, length, canonical id); never depend on set/dict order.

## Checklist
- [ ] Technique validated against the schema.
- [ ] Preconditions cite real graph patterns; effect is a concrete edge/state.
- [ ] At least one cross-cloud technique exercised by a fixture.
- [ ] Output carries score factors and per-step evidence.
