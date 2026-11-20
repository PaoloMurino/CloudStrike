---
inclusion: always
---

# CloudStrike — Technology & Quality Standards

Permanent technical rules (`QA-*`) and the approved stack. Specs and skills reference these rules
by ID rather than restating them. Terms follow the glossary in `product.md`.

## Approved stack

| Layer | Choice | Notes |
| --- | --- | --- |
| Core analysis & agents | **Python 3.11+** | Graph model, rule engine, path analysis, simulation, orchestrator |
| Graph store | Abstract `GraphStore` interface | In-memory implementation for MVP; backend swappable, no engine lock-in |
| Provider access | **Native CSP SDKs/APIs** | AWS (boto3), Azure (azure-sdk / Resource Manager + Microsoft Graph), GCP (google-cloud SDKs). CLI wrappers are forbidden as a dependency (`AG-04`) |
| Probe packaging | Portable container image | Deployable to any CSP, on-prem, Kubernetes, serverless |
| Frontend | **TypeScript + React** | Interactive graph UI |
| Graph visualization | **Cytoscape.js** | Attack-path overlay, before/after diff view |
| Config / data interchange | YAML (scenarios, technique catalog), JSON (API) | Human-authored catalogs are YAML |

Introducing a technology outside this table requires an ADR referenced from `structure.md`; do not add
it silently.

## QA rules

- **QA-01 Determinism.** The same snapshot plus the same technique catalog MUST produce the same
  Findings, attack paths and simulation result. No wall-clock, randomness or ordering dependence in
  analysis output (`AD-04`).
- **QA-02 Testing.** Core analysis (rules, path composition, simulation, remediation diff) MUST have
  unit tests. The simulation engine MUST additionally have property-based tests asserting its
  invariants (determinism, monotonicity of remediation: removing an edge never creates a new path).
- **QA-03 Explainability.** Every Finding, attack path and risk score MUST carry the data that
  justifies it (which permission, which trust, which technique). No opaque scoring (`AD-08`).
- **QA-04 Scoring is explicit.** Risk = likelihood × impact with a documented formula. The formula
  lives in the `attack-path-analysis` spec and is cited, not duplicated.
- **QA-05 No secrets in output.** Logs, snapshots, reports and test fixtures MUST NOT contain real
  secrets, tokens or credentials. Use redactable identifiers (`SEC-03`).
- **QA-06 Definition of done.** A task is done when: its `_Requirements_` are satisfied, tests pass,
  `context-lint` reports no error on the touched artifacts, and no steering rule is violated.
- **QA-07 Provider isolation at build time.** Core packages MUST NOT import any provider SDK; only
  adapters may (`ARC-02`). This is enforced structurally, not by convention alone.
- **QA-08 Catalogs are data.** Techniques and controls are data files validated against a schema, not
  code. Adding one MUST NOT require changing the engine (`AD-05`).
