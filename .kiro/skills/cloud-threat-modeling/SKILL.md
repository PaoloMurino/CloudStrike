---
name: cloud-threat-modeling
description: Use when designing or reviewing a CloudStrike feature, component or attack scenario and you need to reason about threats, trust boundaries and attacker goals in a multi-cloud estate. Applies STRIDE to cloud and maps threats to MITRE ATT&CK Cloud.
---

# Cloud Threat Modeling

Reusable procedure for threat-modeling a CloudStrike capability or a modeled estate. It produces the
threats a design must address; it does not define product rules (those live in steering) or feature
requirements (those live in specs).

## When to use
- Designing a new spec or component and you need its threat surface.
- Reviewing a modeled estate to decide which attack paths matter most.
- Deciding which Controls a simulation step must evaluate.

## Procedure
1. **Set the frame.** Identify assets (Principals, sensitive Resources), entry points (public
   exposure, CI/CD, federation) and trust boundaries, including cross-cloud ones (`MC-03`).
2. **Enumerate with STRIDE-for-cloud.** For each boundary ask: Spoofing (weak federation / OIDC
   subject conditions), Tampering (writable config), Repudiation (missing audit), Information
   disclosure (public exposure, secrets in config), Denial of service (scope-limited, usually out of
   scope), Elevation of privilege (role assumption, impersonation, excessive permissions).
3. **Map to ATT&CK Cloud.** Tag each threat with a MITRE ATT&CK Cloud technique id so it links to the
   technique catalog used by `attack-path-analysis`.
4. **Rank by reachable impact.** Prefer threats that enable cross-cloud movement or reach high-impact
   targets; this feeds the scoring factors in the PATHS spec.
5. **State the defeating Control.** For each threat name the Control that would block it, so
   simulation (`SIM`) and remediation (`REMED`) have a target.

## Checklist
- [ ] Cross-cloud trust boundaries explicitly considered, not just per-provider.
- [ ] Every threat mapped to an ATT&CK Cloud id.
- [ ] Every threat has a candidate defeating Control.
- [ ] No step assumes a live offensive action (Simulated-first, `SEC-02`).

## Boundaries
This skill reasons about threats only. It never proposes running an attack against a real estate and
never weakens a `SEC-*` guardrail.
