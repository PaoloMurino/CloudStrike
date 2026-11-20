---
inclusion: fileMatch
fileMatchPattern: ["src/adapters/azure/**", ".kiro/specs/*/design.md"]
---

# CloudStrike — Azure Provider Specifics

Rules (`PROV-AZ-*`) the Azure adapter and Azure-aware analysis MUST preserve when mapping to the
canonical model (`multicloud-model.md`).

- **PROV-AZ-01 RBAC scope hierarchy.** Effective permissions MUST account for role assignments across
  the management group → subscription → resource group → resource hierarchy, including inheritance and
  **deny assignments** (which override allows).
- **PROV-AZ-02 Entra ID identities.** Users, groups, service principals, managed identities and app
  registrations map to `Principal`. **Federated credentials** on app registrations (workload identity
  federation, e.g. from GitHub OIDC) map to `CAN_ASSUME`/`TRUSTS` with the issuer/subject condition.
- **PROV-AZ-03 Conditional Access & PIM.** Conditional Access policies and **PIM** (eligible vs active
  role activation, MFA requirements) map to `Control` nodes and `PROTECTED_BY` edges.
- **PROV-AZ-04 Read-only roles.** Ingestion uses Reader / Security Reader (`SEC-04`).
- **PROV-AZ-05 Exposure.** Public exposure (NSG rules, public IPs, storage account public access,
  Key Vault access policy / RBAC) maps to `EXPOSES`.
- **PROV-AZ-06 Native SDK.** Azure access uses the azure-sdk (Resource Manager) and Microsoft Graph,
  never the `az` CLI as a dependency (`AG-04`).
