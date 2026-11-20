---
inclusion: fileMatch
fileMatchPattern: ["src/core/**", "catalogs/**", ".kiro/specs/cloud-graph-model/**", ".kiro/specs/attack-path-analysis/**", ".kiro/specs/misconfiguration-detection/**"]
---

# CloudStrike — Canonical Multi-Cloud Model

Rules (`MC-*`) for the common cloud security graph. Loaded when working on core model, catalogs or the
model-related specs. Terms follow `product.md`.

## Node types

The graph has exactly these canonical node types. Provider objects map onto them; they do not add
new top-level types.

- **Principal**, **Resource**, **Permission** (edge-like but first-class when conditional),
  **NetworkBoundary**, **Control**, **Finding**.

## Edge types

- **MC-01 Canonical edges only.** Relationships use this closed set: `CAN_ASSUME`, `HAS_PERMISSION`,
  `TRUSTS`, `REACHES` (network reachability), `EXPOSES` (public/external exposure), `PROTECTED_BY`
  (to a Control). New semantics require an ADR, not an ad-hoc edge.
- **MC-02 Provider specifics are namespaced.** Provider-dependent attributes live under `aws.*`,
  `azure.*`, `gcp.*` on the node/edge. The canonical layer stays provider-neutral (`ARC-01`).

## Cross-cloud trust (the differentiator)

- **MC-03 Trust is first-class and cross-provider.** `CAN_ASSUME` and `TRUSTS` edges MUST be able to
  connect principals across providers: GitHub/OIDC → AWS role, AWS → Azure via stored secret, Azure
  federated credential, GCP Workload Identity Federation. Cross-cloud edges carry the federation
  mechanism as an attribute.
- **MC-04 Reachability is explainable.** Every edge records why it exists (the policy, trust config or
  network rule that justifies it) so Findings and paths can cite it (`QA-03`).

## Invariants

- **MC-05 Determinism.** Model construction from a snapshot is deterministic and order-independent
  (`QA-01`).
- **MC-06 No secrets in the model.** Node/edge attributes never store secret values; a secret is
  represented by a redactable reference (`SEC-03`).
- **MC-07 Snapshot-scoped.** The graph is built from a point-in-time snapshot; analysis never reaches
  back to a live cloud to resolve a node.
