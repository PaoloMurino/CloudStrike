# Attack Simulation — Requirements

Spec code: **SIM**. Executes an attack path step by step over the digital twin, showing which
controls intervene. Supports Simulated (default) and Live/Probe modes.

## Governing rules

Implements `AD-04`, `AD-15`, `AG-05`, `AG-07`, `QA-01`, `QA-02`, `QA-03`, `SEC-01`, `SEC-02`,
`SEC-05`, `SEC-07`. Terms per the `product.md` glossary.

## Requirements

#### REQ-SIM-01 — Deterministic twin execution
WHEN a path is simulated over the same twin and catalog THE SYSTEM SHALL produce an identical,
step-by-step execution trace.

#### REQ-SIM-02 — Control evaluation per step
WHEN executing a step THE SYSTEM SHALL evaluate the Controls on that step and record whether each
would allow or block it, with the reason.

#### REQ-SIM-03 — Blocked-step outcome
WHEN an enforcing Control blocks a step THE SYSTEM SHALL mark the path interrupted at that step and
report the blocking Control.

#### REQ-SIM-04 — Simulated mode is the default and safe
WHEN a simulation is requested without an explicit, valid Authorization Scope THE SYSTEM SHALL run
in Simulated mode and SHALL NOT perform any action against a cloud.

#### REQ-SIM-05 — Live mode requires an authorized scope
WHEN Live mode is requested THE SYSTEM SHALL execute only through a registered probe and only for
steps inside a valid Authorization Scope, and SHALL deny any step outside it.

#### REQ-SIM-06 — Audit of live actions
WHEN a step executes in Live mode THE SYSTEM SHALL write an append-only audit record before and
after the action.

#### REQ-SIM-07 — Explainable trace
WHEN a simulation completes THE SYSTEM SHALL return a trace where every step cites its technique,
evidence and control outcome.
