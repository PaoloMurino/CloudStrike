# Misconfiguration Detection — Requirements

Spec code: **DETECT**. Runs a data-driven rule set over the graph to produce Findings.

## Governing rules

Implements `AD-05`, `AD-08`, `ARC-03`, `MC-04`, `QA-01`, `QA-03`, `QA-08`, `SEC-04`. Terms per the
`product.md` glossary.

## Requirements

#### REQ-DETECT-01 — Data-driven rule set
WHEN detection runs THE SYSTEM SHALL load rules from `catalogs/controls/` as data, AND adding a rule
SHALL NOT require changing engine code.

#### REQ-DETECT-02 — Finding output
WHEN a rule matches THE SYSTEM SHALL emit a Finding node linked to the offending nodes/edges, with
severity, the matched evidence and a remediation hint.

#### REQ-DETECT-03 — Excessive permission detection
WHEN a Principal holds permissions beyond a defined baseline THE SYSTEM SHALL raise an
excessive-permission Finding citing the granting policy.

#### REQ-DETECT-04 — Risky trust detection
WHEN a TRUSTS or CAN_ASSUME edge is overly permissive (e.g. unconstrained OIDC subject, wildcard
principal) THE SYSTEM SHALL raise a risky-trust Finding.

#### REQ-DETECT-05 — Deterministic, explainable output
WHEN the same graph is scanned twice THE SYSTEM SHALL emit identical Findings, each carrying the
evidence that justifies it.
