---
name: security-remediation
description: Use when proposing or validating a remediation for a Finding or an attack path across AWS, Azure or GCP. Expresses remediation as a graph patch, re-simulates to prove the path breaks, and emits suggested IaC as an artifact only, never applied.
---

# Security Remediation

How CloudStrike proposes fixes and proves they work. Pairs with the `REMED` spec. Know-how only.

## When to use
- A Finding or attack path needs a fix.
- Validating that a proposed change actually breaks a path (what-if).
- Generating suggested Terraform for a remediation.

## Procedure
1. **Locate the choke point.** Find the step whose removal breaks the most paths (usually a risky
   trust edge or an excessive permission), using the path's cited evidence (`QA-03`).
2. **Express as a graph patch.** Model the fix as add/remove/modify on the graph: tighten an OIDC
   subject condition, remove a `PassRole`, add an enforcing Control (`REQ-REMED-01`, `AD-07`).
3. **Re-simulate.** Run the same deterministic engine on the patched twin and diff: paths broken,
   paths remaining, any new path (`REQ-REMED-02`, `REQ-REMED-03`).
4. **Check monotonicity.** A removal-only patch must not create a new path; if the diff shows one,
   the model or patch is wrong (`REQ-REMED-04`).
5. **Emit suggested IaC.** Render Terraform as an artifact only. Never apply it (`REQ-REMED-05`,
   `SEC-01`).

## Provider remediation notes
- **AWS**: constrain `sts:AssumeRoleWithWebIdentity` trust (`sub`/`aud`), add permission boundary, add
  an SCP deny.
- **Azure**: tighten federated-credential subject, remove excessive role assignment, add a deny
  assignment or Conditional Access.
- **GCP**: narrow the WIF attribute condition, remove an impersonation binding, add an IAM deny policy.

## Checklist
- [ ] Remediation is a graph patch, not a live change.
- [ ] Before/after delta proves the target path is broken.
- [ ] Monotonicity holds for removal-only patches.
- [ ] IaC is output only, never applied.
