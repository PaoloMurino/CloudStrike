# Probe Lifecycle — Tasks

- [ ] 1. Implement the portable probe runtime and container packaging (deploy anywhere).
  _Requirements: REQ-PROBE-01, REQ-PROBE-02_

- [ ] 2. Implement registration to the Control Plane with identity and declared scope.
  _Requirements: REQ-PROBE-01_

- [ ] 3. Implement the authorization check (target, action, time window) gating every action.
  _Requirements: REQ-PROBE-03, REQ-PROBE-04_

- [ ] 4. Implement the executor as the sole Live actor, calling adapters only post-authorization.
  _Requirements: REQ-PROBE-04, REQ-PROBE-07_

- [ ] 5. Implement the append-only audit sink.
  _Requirements: REQ-PROBE-05_

- [ ] 6. Implement the kill switch with precedence over running plans.
  _Requirements: REQ-PROBE-06_

- [ ] 7. Tests: out-of-scope denial, sole-actor path, audit coverage, revoke, no-CLI-dependency.
  _Requirements: REQ-PROBE-02, REQ-PROBE-03, REQ-PROBE-04, REQ-PROBE-05, REQ-PROBE-06_
