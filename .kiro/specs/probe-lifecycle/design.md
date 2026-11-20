# Probe Lifecycle — Design

Implements `requirements.md`. Rules cited by ID (see `agent-architecture.md`, `security-guardrails.md`).

## Modules

- `probes/runtime.py` — portable probe entrypoint; packaged as a container image deployable anywhere
  (`REQ-PROBE-01`).
- `probes/registration.py` — register to the Control Plane with identity + declared scope
  (`REQ-PROBE-01`).
- `probes/authorization.py` — the scope check (target, allowed action, time window) that every
  action passes before reaching an adapter (`REQ-PROBE-03`, `ARC-05`, `SEC-09`).
- `probes/executor.py` — the sole Live actor; calls `adapters/*` action APIs only after authorization
  and audit (`REQ-PROBE-04`).
- `probes/audit.py` — append-only audit sink (`REQ-PROBE-05`).
- `probes/revoke.py` — kill switch honored ahead of any running plan (`REQ-PROBE-06`).

## Key decisions

- **Adapters never self-authorize** (`SEC-09`): the action path is `agent → executor → authorization
  → adapter`. There is no shortcut.
- **Native SDKs only** (`REQ-PROBE-02`, `AG-04`): CLI tools are excluded from runtime dependencies;
  an import/dependency test enforces this.
- **Least privilege** (`REQ-PROBE-07`, `SEC-04`): the scope declares the minimal action set;
  provisioning maps it to the narrowest provider role.
- Revocation is checked at the top of the executor loop and interrupts in-flight work (`REQ-PROBE-06`).

## Properties to test

- Out-of-scope action (wrong target / action / time window) is denied before any adapter call.
- No mutating adapter call exists outside the executor path (`REQ-PROBE-04`).
- Every action produces an audit record (`REQ-PROBE-05`).
- Revoke stops subsequent actions (`REQ-PROBE-06`).
- No CLI tool in runtime dependencies (`REQ-PROBE-02`).
