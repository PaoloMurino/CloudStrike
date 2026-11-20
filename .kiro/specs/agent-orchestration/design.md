# Agent Orchestration — Design

Implements `requirements.md`. Rules cited by ID (see `agent-architecture.md`).

## Modules

- `agents/control_plane.py` — goal intake, task decomposition, delegation, aggregation
  (`REQ-ORCH-01`, `REQ-ORCH-02`).
- `agents/base.py` — the plan–act–observe loop and step recorder shared by all agents
  (`REQ-ORCH-03`).
- `agents/{recon,iam,paths,execution,remediation}.py` — one capability each (`AG-02`), calling
  `core/*` and, for Live, the probe executor via `probes/` (`ARC-04`).
- `agents/task.py` — task envelope carrying `mode` (Simulated|Live) and optional scope ref
  (`REQ-ORCH-04`).

## Key decisions

- The Control Plane is the only coordinator; agents expose typed handlers and return results to it
  (`REQ-ORCH-02`).
- Mode defaults to Simulated; promotion to Live requires a covering scope resolved by the
  simulation/probe layer (`REQ-ORCH-04`, fail-closed, `SEC-02`).
- Bounded autonomy is enforced in `base.py`: an agent cannot issue a task to itself or request
  credentials; only the Control Plane creates tasks (`REQ-ORCH-05`, `SEC-10`).
- Planning over the model is deterministic (`REQ-ORCH-06`, `QA-01`); only Live timing may vary.

## Properties to test

- A goal decomposes to the expected capability tasks.
- No agent-to-agent call path exists (coordination only via Control Plane).
- Same twin+catalog ⇒ identical plan (determinism).
- An out-of-task discovered path produces a report, not an action.
