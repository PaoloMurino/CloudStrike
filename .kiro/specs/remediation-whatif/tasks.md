# Remediation What-If — Tasks

- [ ] 1. Implement `GraphPatch` applied to a twin copy, leaving the snapshot immutable.
  _Requirements: REQ-REMED-01_

- [ ] 2. Implement the what-if runner: apply patch, re-simulate, diff paths.
  _Requirements: REQ-REMED-02, REQ-REMED-03_

- [ ] 3. Implement explainable delta citing interrupted steps and the responsible change.
  _Requirements: REQ-REMED-06_

- [ ] 4. Implement suggested-IaC rendering as an artifact only (never applied).
  _Requirements: REQ-REMED-05_

- [ ] 5. Property tests: snapshot immutability, monotonicity, deterministic delta.
  _Requirements: REQ-REMED-01, REQ-REMED-03, REQ-REMED-04_
