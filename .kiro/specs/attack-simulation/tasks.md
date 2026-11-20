# Attack Simulation — Tasks

- [ ] 1. Implement the deterministic step-by-step twin execution engine.
  _Requirements: REQ-SIM-01, REQ-SIM-07_

- [ ] 2. Implement per-step Control evaluation and the blocked-step (interrupted path) outcome.
  _Requirements: REQ-SIM-02, REQ-SIM-03_

- [ ] 3. Implement mode resolution (fail-closed to Simulated without a valid scope).
  _Requirements: REQ-SIM-04_

- [ ] 4. Implement the probe executor as the sole Live actor, gated by scope check.
  _Requirements: REQ-SIM-05_

- [ ] 5. Implement append-only audit around every Live action.
  _Requirements: REQ-SIM-06_

- [ ] 6. Property tests: determinism, fail-closed, out-of-scope denial, enforcing-control interrupt.
  _Requirements: REQ-SIM-01, REQ-SIM-03, REQ-SIM-04, REQ-SIM-05_
