---
name: multicloud-iam-analysis
description: Use when analyzing permissions, roles, trust or federation across AWS, Azure and GCP, or when building an IAM-aware adapter or detection rule. Explains how to compute effective permissions per provider and how to normalize cross-cloud assumption and federation into canonical edges.
---

# Multi-Cloud IAM Analysis

How CloudStrike reasons about identity and access across providers, and how it normalizes them into
the canonical model (`multicloud-model.md`). Know-how only; rules stay in steering.

## When to use
- Building or reviewing an IAM ingestion adapter.
- Writing excessive-permission or risky-trust detection rules (`DETECT`).
- Defining CAN_ASSUME / TRUSTS techniques for attack paths (`PATHS`).

## Effective permissions per provider
- **AWS** (`PROV-AWS-01`): intersect identity + resource policies, subtract permission boundaries and
  SCPs; an explicit deny anywhere wins. Session policies narrow further.
- **Azure** (`PROV-AZ-01`): resolve RBAC across management group → subscription → resource group →
  resource, including inheritance; deny assignments override allows. Account for Conditional Access
  and PIM eligible-vs-active (`PROV-AZ-03`).
- **GCP** (`PROV-GCP-01`): resolve IAM across org → folder → project → resource, including IAM
  Conditions and deny policies.

## Cross-cloud normalization (the differentiator)
Map every assumption/federation to a CAN_ASSUME or TRUSTS edge with a `federation` attribute
(`MC-03`):
- AWS `AssumeRoleWithWebIdentity` (GitHub OIDC) → `oidc`, carrying `sub`/`aud`/condition.
- Azure federated credential on an app registration → `federated-credential`, carrying issuer/subject.
- GCP Workload Identity Federation (from AWS/Azure/OIDC) → `wif`, carrying pool/provider condition.
- A secret of one cloud stored in another → `stored-secret` edge from the storing Resource.

## Privilege-escalation patterns to flag
- `iam:PassRole` + a compute service that assumes the passed role (AWS).
- Service account impersonation chains (`PROV-GCP-02`).
- App-registration owner able to add a federated credential (Azure).
- Unconstrained OIDC subject (`repo:*`) in a trust policy.

## Checklist
- [ ] Denies (SCP, deny assignment, deny policy) applied before concluding access.
- [ ] Every cross-cloud edge carries its `federation` mechanism and condition.
- [ ] Effective-permission conclusion cites the granting policy as evidence (`MC-04`).

## Boundaries
Read-only reasoning over the model (`SEC-04`). Never attempt a real assumption/impersonation outside
an authorized probe scope (`SEC-05`).
