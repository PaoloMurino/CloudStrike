---
inclusion: fileMatch
fileMatchPattern: ["src/agents/**", "src/probes/**", ".kiro/specs/agent-orchestration/**", ".kiro/specs/probe-lifecycle/**"]
---

# CloudStrike — Agentic Architecture

Rules (`AG-*`) for the Control Plane, the specialized agents and the probes. Loaded when working on
agent/probe code or their specs. Terms follow `product.md`; security is governed by `security-guardrails.md`.

## Topology

- **AG-01 Control Plane orchestrates.** A central Control Plane plans work, decomposes a goal into
  tasks, delegates to specialized agents, and aggregates results. Agents do not coordinate peer-to-peer;
  they report to the Control Plane.
- **AG-02 One capability per agent.** Specialized agents map one-to-one to capabilities: `recon`
  (ingestion via adapters), `iam-analysis`, `attack-path`, `execution`, `remediation`. An agent owns
  its capability end to end and exposes a typed interface.
- **AG-03 Plan–act–observe loop.** Each agent runs an explicit loop: plan the next step, act (call
  `core/*` or, in Live mode, a probe), observe the result, decide whether to continue. Every step is
  recorded so a run is replayable and explainable (`QA-03`).

## Probes

- **AG-04 Native CSP APIs only.** Probes and adapters use native provider SDKs/APIs. CLI tools
  (`aws`, `az`, `gcloud`, `terraform`) MUST NOT be a runtime dependency. They may appear only in
  developer docs.
- **AG-05 Deploy anywhere, register back.** A probe is a portable artifact the customer deploys where
  they choose (any CSP, on-prem, Kubernetes, serverless). On start it registers to the Control Plane
  with its identity and declared Authorization Scope (`SEC-05`), then receives tasks.
- **AG-06 Probe is the only actor in Live mode.** The Control Plane and agents never call a cloud
  mutating API directly. All Live actions go through a registered probe, which enforces the scope
  before calling an adapter (`ARC-05`, `SEC-09`).
- **AG-07 Simulated vs Live is explicit per task.** Every delegated task carries its execution mode.
  Simulated tasks run against the digital twin and never reach a probe. A task may be promoted to Live
  only if a covering Authorization Scope exists; otherwise it stays Simulated.

## Behavior

- **AG-08 Bounded autonomy.** An agent completes the delegated task and reports. It MUST NOT widen
  scope, acquire new credentials, or pursue a discovered path beyond its task without the Control
  Plane issuing a new, scoped task (`SEC-10`).
- **AG-09 Deterministic planning in Simulated mode.** Given the same twin and catalogs, agent planning
  over the model is reproducible (`QA-01`). Non-determinism is allowed only in Live timing, never in
  analysis conclusions.
