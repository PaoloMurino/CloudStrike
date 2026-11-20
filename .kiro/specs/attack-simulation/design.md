# Attack Simulation — Design

Implements `requirements.md`. Rules cited by ID. Security is governed by `security-guardrails.md`.

## Modules

- `core/simulation/engine.py` — walks a path step by step over the twin, evaluating Controls
  (`REQ-SIM-01`, `REQ-SIM-02`, `REQ-SIM-03`); pure, deterministic, no side effects.
- `core/simulation/trace.py` — structured, explainable execution trace (`REQ-SIM-07`).
- `core/simulation/mode.py` — resolves execution mode: Simulated unless a valid Authorization Scope
  is supplied (`REQ-SIM-04`, `AG-07`).
- `probes/executor.py` — the only component that performs Live actions, gated by the scope check and
  audit (`REQ-SIM-05`, `REQ-SIM-06`, `ARC-05`, `SEC-09`).

## Key decisions

- **Simulated vs Live is a per-step decision** carried by the task (`AG-07`). The core engine never
  calls a probe; it asks the executor only when a step is Live and scope-covered.
- **Fail-closed** (`REQ-SIM-04`, `SEC-02`): absent/invalid scope ⇒ Simulated. There is no path from a
  generic request to a Live action.
- **Control model**: a Control on a step has an `enforcing` flag; only enforcing Controls block
  (`REQ-SIM-03`). Detective-only Controls are recorded but do not interrupt.

## Properties to test (QA-02)

- Determinism: same twin+path ⇒ identical trace (`REQ-SIM-01`).
- Fail-closed: request without scope never reaches the executor (`REQ-SIM-04`).
- Out-of-scope step is denied in Live mode (`REQ-SIM-05`).
- Enforcing Control interrupts the path at the right step (`REQ-SIM-03`).
