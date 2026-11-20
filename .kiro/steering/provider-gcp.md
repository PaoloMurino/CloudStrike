---
inclusion: fileMatch
fileMatchPattern: ["src/adapters/gcp/**", ".kiro/specs/*/design.md"]
---

# CloudStrike — GCP Provider Specifics

Rules (`PROV-GCP-*`) the GCP adapter and GCP-aware analysis MUST preserve when mapping to the
canonical model (`multicloud-model.md`).

- **PROV-GCP-01 Resource hierarchy.** Effective permissions MUST account for IAM policy inheritance
  across organization → folder → project → resource, including **IAM Conditions** and **deny
  policies**.
- **PROV-GCP-02 Service account impersonation.** `iam.serviceAccounts.getAccessToken`,
  `actAs`, `signJwt` and `getOpenIdToken` map to `CAN_ASSUME` edges between principals and service
  accounts, carrying the granting binding.
- **PROV-GCP-03 Workload Identity Federation.** WIF (from AWS, Azure, GitHub OIDC, OIDC/SAML IdPs)
  maps to cross-cloud `CAN_ASSUME`/`TRUSTS` edges, carrying the pool/provider attribute condition
  (`MC-03`).
- **PROV-GCP-04 Read-only roles.** Ingestion uses Viewer / Security Reviewer (`SEC-04`).
- **PROV-GCP-05 Exposure.** Public exposure (`allUsers`/`allAuthenticatedUsers` bindings, firewall
  rules 0.0.0.0/0, public GCS buckets, public Cloud Run/Functions) maps to `EXPOSES`.
- **PROV-GCP-06 Native SDK.** GCP access uses the google-cloud client libraries, never the `gcloud`
  CLI as a dependency (`AG-04`).
