---
inclusion: fileMatch
fileMatchPattern: ["src/adapters/aws/**", ".kiro/specs/*/design.md"]
---

# CloudStrike — AWS Provider Specifics

Rules (`PROV-AWS-*`) the AWS adapter and AWS-aware analysis MUST preserve when mapping to the
canonical model (`multicloud-model.md`). These capture what the common model must not flatten away.

- **PROV-AWS-01 Full policy evaluation.** Effective permissions MUST account for identity policies,
  resource policies, **permission boundaries**, **Service Control Policies (SCPs)** and session
  policies. An explicit deny anywhere wins. Do not approximate with identity policies alone.
- **PROV-AWS-02 Role assumption.** `sts:AssumeRole`, `AssumeRoleWithWebIdentity` (OIDC) and
  `AssumeRoleWithSAML` map to `CAN_ASSUME` edges, carrying the trust policy and its conditions
  (`aws:PrincipalOrgID`, `sub`, `aud`, external ID) as attributes.
- **PROV-AWS-03 Read-only roles.** Ingestion uses SecurityAudit / ViewOnlyAccess. No mutating API in
  the read path (`SEC-04`).
- **PROV-AWS-04 Exposure.** Public exposure (S3 bucket policy/ACL/Block Public Access, security
  groups 0.0.0.0/0, public ALB/API Gateway) maps to `EXPOSES`, recording the rule that opens it.
- **PROV-AWS-05 Native SDK.** AWS access uses boto3 / AWS SDK, never the `aws` CLI as a dependency
  (`AG-04`).
- **PROV-AWS-06 Account/Org hierarchy.** Organization, OU and account context is preserved so
  cross-account trust and SCP scoping are evaluated correctly.
