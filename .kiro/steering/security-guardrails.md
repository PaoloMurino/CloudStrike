---
inclusion: always
---

# CloudStrike — Security Guardrails & Authorization Model

Non-negotiable security rules (`SEC-*`). These override convenience, speed and any instruction in a
spec, skill or user prompt. When a request conflicts with a `SEC-*` rule, refuse the unsafe part and
offer the Simulated-mode alternative. Terms follow `product.md`.

## Core guardrails

- **SEC-01 No unauthorized mutation.** CloudStrike MUST NOT perform any action that changes a cloud
  estate (create / update / delete / assume / impersonate) unless it runs through an authorized
  probe inside a valid Authorization Scope (`SEC-05`). Customer production estates are read-only.
- **SEC-02 Simulation first.** Attack reasoning runs in Simulated mode over the digital twin by
  default. Live execution is never the default and is never implied by a generic request like
  "attack X". Such a request MUST be answered with a Simulated run.
- **SEC-03 No secrets at rest or in output.** Secrets, tokens and credentials MUST NOT be written to
  logs, snapshots, reports, datasets or test fixtures. Snapshots are encrypted at rest. Identifiers
  that may be sensitive are redactable (`QA-05`).
- **SEC-04 Least privilege for access.** Read/ingestion uses read-only roles only (AWS SecurityAudit
  or ViewOnly, Azure Reader / Security Reader, GCP Viewer / Security Reviewer). A probe receives only
  the credentials its Authorization Scope requires, nothing broader.

## Authorization model (Live / Probe mode)

Live actions exist in the product vision but are gated by this model. They are out of the hackathon
demo (which stays Simulated).

- **SEC-05 Explicit Authorization Scope.** Every Live action MUST be covered by an Authorization
  Scope declared before execution, specifying: target (account / subscription / project), the exact
  set of allowed actions, and a time window. An action outside any of these three dimensions is
  denied. There is no implicit or inherited scope.
- **SEC-06 Ownership / authorization proof.** A scope is valid only for a target the customer owns or
  is explicitly authorized to test. Absent proof, the action is denied.
- **SEC-07 Immutable audit.** Every Live action (requested, allowed, denied, executed, result) MUST
  be recorded in an append-only audit trail before and after execution. No Live action without an
  audit record.
- **SEC-08 Kill switch.** Every probe MUST honor an immediate revoke that stops in-flight and future
  actions. Revocation takes precedence over any running plan.
- **SEC-09 Native API only, scoped.** Probes act via native CSP APIs (`AG-04`). An action call MUST
  pass the authorization check (`ARC-05`) before reaching an adapter; adapters never self-authorize.

## Agent behavior

- **SEC-10 No autonomous escalation.** An agent MUST NOT expand its own Authorization Scope, request
  broader credentials, or chain into a target outside the scope, even if an attack path suggests it
  is possible. It reports the path; it does not walk it without a covering scope.
- **SEC-11 Refuse offensive work off-target.** Requests to attack, scan or exploit a system the user
  does not own or has no scope for MUST be refused, regardless of claimed intent.

## How this is enforced

These rules are backed by hooks (see `.kiro/hooks/`): a `PreToolUse` guard blocks mutating cloud
commands, and a pre-execution gate blocks actions lacking a declared scope. Rules here are the single
source; hooks and specs reference them by ID and MUST NOT restate the logic.
