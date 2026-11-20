# Probe Lifecycle — Requirements

Spec code: **PROBE**. Deployable probes that register to the Control Plane and perform Live actions
via native CSP APIs within an Authorization Scope.

## Governing rules

Implements `AD-12`, `AD-13`, `AD-14`, `AG-04`, `AG-05`, `AG-06`, `ARC-05`, `SEC-04`, `SEC-05`,
`SEC-06`, `SEC-07`, `SEC-08`, `SEC-09`. Terms per the `product.md` glossary.

## Requirements

#### REQ-PROBE-01 — Deploy anywhere, register back
WHEN a probe starts THE SYSTEM SHALL let it run in any CSP, on-prem, Kubernetes or serverless target
and SHALL register it to the Control Plane with its identity and declared Authorization Scope.

#### REQ-PROBE-02 — Native CSP APIs only
WHEN a probe acts THE SYSTEM SHALL use native CSP SDKs/APIs, AND SHALL NOT depend on cloud CLI tools
at runtime.

#### REQ-PROBE-03 — Scope enforcement before action
WHEN a probe is asked to perform an action THE SYSTEM SHALL verify the action is within its
Authorization Scope (target, allowed action, time window) before calling an adapter, and SHALL deny
anything outside it.

#### REQ-PROBE-04 — Probe is the only Live actor
WHEN any Live action is required THE SYSTEM SHALL perform it only through a registered probe, AND the
Control Plane and agents SHALL NOT call a mutating cloud API directly.

#### REQ-PROBE-05 — Immutable audit
WHEN a probe handles an action (requested, allowed, denied, executed, result) THE SYSTEM SHALL write
an append-only audit record.

#### REQ-PROBE-06 — Kill switch
WHEN a revoke is issued for a probe THE SYSTEM SHALL immediately stop its in-flight and future
actions, taking precedence over any running plan.

#### REQ-PROBE-07 — Least-privilege credentials
WHEN a probe is provisioned THE SYSTEM SHALL grant only the credentials its Authorization Scope
requires and no broader.
