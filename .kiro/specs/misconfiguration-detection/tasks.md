# Misconfiguration Detection — Tasks

- [ ] 1. Define the rule YAML schema and loader.
  _Requirements: REQ-DETECT-01_

- [ ] 2. Implement the rule engine emitting Finding nodes with evidence and remediation hints.
  _Requirements: REQ-DETECT-02, REQ-DETECT-05_

- [ ] 3. Implement permission baselines and excessive-permission detection.
  _Requirements: REQ-DETECT-03_

- [ ] 4. Implement risky-trust detection on federation/condition attributes.
  _Requirements: REQ-DETECT-04_

- [ ] 5. Seed an initial control catalog (public exposure, excessive permission, risky trust).
  _Requirements: REQ-DETECT-01, REQ-DETECT-03, REQ-DETECT-04_

- [ ] 6. Tests: data-driven extensibility, determinism, excessive-permission and risky-trust fixtures.
  _Requirements: REQ-DETECT-01, REQ-DETECT-03, REQ-DETECT-04, REQ-DETECT-05_
