# Agent Orchestration — Requirements

Spec code: **ORCH**. The Control Plane that plans work and delegates to specialized agents.

## Governing rules

Implements `AD-11`, `AG-01`, `AG-02`, `AG-03`, `AG-07`, `AG-08`, `AG-09`, `ARC-04`, `QA-01`, `QA-03`,
`SEC-02`, `SEC-10`. Terms per the `product.md` glossary.

## Requirements

#### REQ-ORCH-01 — Goal decomposition
WHEN a goal is submitted THE SYSTEM SHALL decompose it into tasks and delegate each to the agent
owning the relevant capability (recon, iam-analysis, attack-path, execution, remediation).

#### REQ-ORCH-02 — Central coordination
WHEN agents run THE SYSTEM SHALL route all coordination through the Control Plane, AND agents SHALL
NOT coordinate peer-to-peer.

#### REQ-ORCH-03 — Plan–act–observe with a recorded trace
WHEN an agent executes a task THE SYSTEM SHALL record each plan/act/observe step so the run is
replayable and explainable.

#### REQ-ORCH-04 — Execution mode per task
WHEN the Control Plane delegates a task THE SYSTEM SHALL tag it Simulated or Live, defaulting to
Simulated unless a valid Authorization Scope covers it.

#### REQ-ORCH-05 — Bounded autonomy
WHEN an agent discovers a path beyond its task THE SYSTEM SHALL report it and SHALL NOT widen its
scope, acquire new credentials or pursue it without a new scoped task from the Control Plane.

#### REQ-ORCH-06 — Deterministic planning in Simulated mode
WHEN planning over the same twin and catalogs in Simulated mode THE SYSTEM SHALL produce the same
plan.
