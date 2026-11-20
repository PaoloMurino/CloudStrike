# Attack Path Analysis — Tasks

- [ ] 1. Define the technique YAML schema and loader with validation (reject missing fields).
  _Requirements: REQ-PATHS-01, REQ-PATHS-02_

- [ ] 2. Implement precondition matcher returning bindings + cited evidence.
  _Requirements: REQ-PATHS-03_

- [ ] 3. Implement the path engine with technique composition and deterministic frontier ordering.
  _Requirements: REQ-PATHS-04, REQ-PATHS-06, REQ-PATHS-07_

- [ ] 4. Implement the risk scoring module per the documented formula, attaching factors.
  _Requirements: REQ-PATHS-05_

- [ ] 5. Seed an initial catalog including one cross-cloud technique (OIDC/WIF federation).
  _Requirements: REQ-PATHS-01, REQ-PATHS-04_

- [ ] 6. Tests: data-driven extensibility, determinism, cross-cloud composition, explainability.
  _Requirements: REQ-PATHS-01, REQ-PATHS-04, REQ-PATHS-05, REQ-PATHS-06_
