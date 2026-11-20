# Remediation What-If — Design

Implements `requirements.md`. Rules cited by ID.

## Modules

- `core/remediation/patch.py` — a `GraphPatch` (add/remove/modify) applied to a copy of the twin;
  the original snapshot is never mutated (`REQ-REMED-01`).
- `core/remediation/whatif.py` — apply patch → re-run `core/simulation` → diff paths
  (`REQ-REMED-02`, `REQ-REMED-03`).
- `core/remediation/iac.py` — render suggested Terraform as a text artifact only (`REQ-REMED-05`).

## Key decisions

- Reuses the deterministic simulation engine unchanged (`AD-04`, `QA-01`), so before/after is
  comparable by construction.
- **Monotonicity** (`REQ-REMED-04`): a removal-only patch is asserted in a property test to never add
  a path (`QA-02`).
- The delta cites interrupted steps and the responsible change, reusing simulation trace evidence
  (`REQ-REMED-06`).
- No real-cloud mutation anywhere (`REQ-REMED-01`, `REQ-REMED-05`, `SEC-01`).

## Properties to test (QA-02)

- Patch leaves the original snapshot unchanged.
- Removal-only patch never introduces a new path (monotonicity).
- Before/after delta is deterministic for the same patch.
