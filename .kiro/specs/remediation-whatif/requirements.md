# Remediation What-If — Requirements

Spec code: **REMED**. Applies a remediation as a patch to the graph, re-runs simulation and reports
the before/after delta.

## Governing rules

Implements `AD-07`, `AD-04`, `QA-01`, `QA-02`, `QA-03`, `SEC-01`. Terms per the `product.md` glossary.

## Requirements

#### REQ-REMED-01 — Remediation as a graph patch
WHEN a remediation is proposed THE SYSTEM SHALL represent it as a patch to the graph (add/remove/
modify nodes or edges) without mutating any real cloud.

#### REQ-REMED-02 — Re-simulation on the patched twin
WHEN a patch is applied THE SYSTEM SHALL re-run the affected attack paths on the patched twin using
the same deterministic engine.

#### REQ-REMED-03 — Before/after delta
WHEN re-simulation completes THE SYSTEM SHALL report which paths were broken, which remain and any
new paths introduced, with the risk delta.

#### REQ-REMED-04 — Monotonicity guard
WHEN a patch only removes edges/permissions THE SYSTEM SHALL NOT report a newly created attack path
as a result of that removal.

#### REQ-REMED-05 — Suggested IaC is never applied
WHEN suggested IaC is generated THE SYSTEM SHALL output it as an artifact only and SHALL NOT apply
it to any cloud.

#### REQ-REMED-06 — Explainable remediation
WHEN a remediation breaks a path THE SYSTEM SHALL cite the step it interrupts and the control or
configuration change responsible.
