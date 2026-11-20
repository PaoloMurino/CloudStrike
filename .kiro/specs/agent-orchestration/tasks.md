# Agent Orchestration — Tasks

- [ ] 1. Implement the Control Plane: goal intake, decomposition, delegation, aggregation.
  _Requirements: REQ-ORCH-01, REQ-ORCH-02_

- [ ] 2. Implement the shared plan–act–observe loop with a recorded, replayable trace.
  _Requirements: REQ-ORCH-03_

- [ ] 3. Implement the five specialized agents, one capability each, calling core/probes.
  _Requirements: REQ-ORCH-01_

- [ ] 4. Implement the task envelope with per-task mode and fail-closed default to Simulated.
  _Requirements: REQ-ORCH-04_

- [ ] 5. Enforce bounded autonomy (no self-tasking, no credential acquisition) in the base agent.
  _Requirements: REQ-ORCH-05_

- [ ] 6. Tests: decomposition, no peer-to-peer, determinism, out-of-task report-not-act.
  _Requirements: REQ-ORCH-02, REQ-ORCH-05, REQ-ORCH-06_
