---
name: attack-scenario-design
description: Use when creating a synthetic lab estate, a demo scenario, or a dataset for testing detection, paths, simulation or remediation. Produces isolated, authorized, lab-only scenarios and never targets real infrastructure.
---

# Attack Scenario Design

How to build the synthetic estates and scenarios CloudStrike runs against. Lab-only, Simulated-first.

## When to use
- Seeding `datasets/` with a synthetic snapshot.
- Designing the cross-cloud demo scenario.
- Creating a fixture that exercises a specific technique or control.

## Scenario shape
A scenario is a snapshot (canonical nodes/edges) plus an intended narrative:
- entry point (e.g. CI/CD OIDC identity),
- the misconfigurations/trusts that enable movement,
- the target (high-impact Principal or Resource),
- the Control that, once added, breaks the path (for the remediation demo).

## Lab-only checklist (non-negotiable)
- [ ] All identifiers are synthetic; no real account/subscription/project ids, no real secrets
      (`SEC-03`).
- [ ] The scenario is self-contained in `datasets/`; nothing points at a live estate.
- [ ] Any "attack" is expressed as graph reachability for Simulated mode (`SEC-02`); no instruction
      to run a real action.
- [ ] If a Live variant is described, it is marked as requiring an Authorization Scope (`SEC-05`) and
      an owned/authorized target (`SEC-06`), and is excluded from the demo.

## Reference demo scenario (cross-cloud)
GitHub Actions OIDC → over-permissive AWS role → Azure service-principal secret stored in an S3
bucket → Azure subscription → GCP via Workload Identity Federation. Remediation: constrain the OIDC
trust policy subject; re-simulate to show the path broken (`REMED`).

## Boundaries
This skill produces data and narrative only. It never generates offensive payloads and never targets
infrastructure the user does not own.
