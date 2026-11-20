# Cloud Graph Model — Requirements

Spec code: **GRAPH**. Builds the canonical, provider-neutral security graph from read-only
snapshots of AWS, Azure and GCP.

## Governing rules

Implements `AD-01`, `AD-02`, `ARC-01`, `ARC-02`, `MC-01`, `MC-02`, `MC-03`, `MC-04`, `MC-05`,
`MC-06`, `MC-07`, `SEC-03`, `SEC-04`, `QA-07`. Provider mapping follows `PROV-AWS-02`, `PROV-AZ-02`,
`PROV-GCP-02`. Terms per the `product.md` glossary.

## Requirements

#### REQ-GRAPH-01 — Canonical node and edge types
WHEN an estate is ingested THE SYSTEM SHALL represent it using only the canonical node types
(Principal, Resource, Permission, NetworkBoundary, Control, Finding) and the closed edge set
(CAN_ASSUME, HAS_PERMISSION, TRUSTS, REACHES, EXPOSES, PROTECTED_BY).

#### REQ-GRAPH-02 — Namespaced provider attributes
WHEN a provider object is mapped THE SYSTEM SHALL keep provider-specific fields under the `aws.*`,
`azure.*` or `gcp.*` namespace and SHALL NOT introduce provider-specific top-level node types.

#### REQ-GRAPH-03 — Read-only ingestion via adapters
WHEN ingesting an estate THE SYSTEM SHALL use a per-provider adapter calling native CSP read APIs
with read-only roles, AND the core SHALL NOT import any provider SDK.

#### REQ-GRAPH-04 — Cross-cloud trust edges
WHEN a federation or assumption relationship exists across providers THE SYSTEM SHALL create a
CAN_ASSUME or TRUSTS edge carrying the federation mechanism as an attribute.

#### REQ-GRAPH-05 — Explainable edges
WHEN any edge is created THE SYSTEM SHALL record the policy, trust configuration or network rule
that justifies it, so downstream Findings and paths can cite it.

#### REQ-GRAPH-06 — Deterministic, snapshot-scoped build
WHEN the same snapshot is ingested twice THE SYSTEM SHALL produce an identical graph, AND SHALL NOT
contact a live cloud during analysis.

#### REQ-GRAPH-07 — No secrets in the model
WHEN a secret value is encountered THE SYSTEM SHALL store a redactable reference instead of the
value, in the graph and in any persisted snapshot.
