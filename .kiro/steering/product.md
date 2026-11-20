---
inclusion: always
---

# CloudStrike — Product Context

CloudStrike is an **agentic, multi-cloud Cloud Security Validation platform** for AWS,
Microsoft Azure and Google Cloud. It builds a unified model of a customer's cloud estate,
finds the paths an attacker could take across providers, and proves which remediation breaks
those paths — before an attacker does.

This file is the shared source of truth for vision, users, scope and vocabulary. Every other
artifact (specs, skills, hooks) reuses the glossary defined here instead of re-defining terms.

## Vision

Show, before an attacker does, which compromise paths exist in a multi-cloud estate, and prove
in measurable terms which change interrupts them.

## Product objectives

1. A single, queryable model of the AWS, Azure and GCP estate: identities, resources, network, trust.
2. Detection of misconfigurations, excessive permissions and risky trust, including across providers.
3. Attack-path computation with explicit, explainable preconditions.
4. Deterministic, reproducible execution of those paths, showing which controls intervene.
5. Remediation proposed as changes to the model, then re-execution and before/after comparison.
6. An agentic delivery model: an orchestrator coordinating specialized agents and deployable probes.

## Agentic by design

CloudStrike is not a batch scanner. It is a system of cooperating agents. Detailed rules live in
`agent-architecture.md` (`AG-*`); the high-level shape is:

- A central **Control Plane** (the orchestrator) plans work and delegates to specialized agents.
- **Specialized agents** own one capability each: reconnaissance, IAM analysis, attack-path
  analysis, execution, remediation.
- **Probes** are deployable units the customer installs where they choose (any CSP, on-prem,
  Kubernetes, serverless). They register to the Control Plane and act near the target using the
  **native CSP APIs** — never CLI wrappers as a dependency.

## Execution modes

CloudStrike has exactly two execution modes (`AG-05`, `SEC-05`):

- **Simulated** (default): reasoning over the graph / digital twin. No calls that change a cloud.
  Always safe, always reproducible. The hackathon demo runs in this mode.
- **Live / Probe**: real actions performed by a customer-deployed probe via native CSP APIs,
  allowed **only** inside an explicitly authorized scope. Governed by the authorization model in
  `security-guardrails.md`.

Customer production estates are always read-only and analyzed in Simulated mode. Live actions only
ever happen through an authorized probe the customer deployed on a target they own.

## Users

| Persona | What they need from CloudStrike |
| --- | --- |
| Cloud Security Architect | Attack paths, cross-cloud trust, evaluation of architectural remediation |
| Cloud / Platform Engineer (DevSecOps) | Concrete remediation, suggested IaC, impact of a change |
| Red / Purple team | Simulated attack scenarios and a technique catalog mapped to MITRE ATT&CK Cloud |
| CISO / Auditor | Before/after reports and measured risk reduction |

## Scope

**In scope**
- Read-only ingestion (provider APIs, exports or IaC) via native CSP APIs.
- Synthetic lab datasets for development and demo.
- Canonical cloud security graph across AWS, Azure, GCP.
- Rule engine producing Findings.
- Attack-path analysis with an explainable technique catalog.
- Simulation over the digital twin (Simulated mode).
- Control mapping and what-if remediation with before/after comparison.
- Agentic orchestration and probe lifecycle (deploy, register, authorize, revoke) as product design.

**Out of scope**
- Executing exploits or payloads against estates the customer does not own or has not authorized.
- Any write to a customer's production cloud.
- Continuous runtime CSPM / on-host agents.
- Full compliance certification.

**Boundary**
- Simulated mode evaluates reachability on the model; it never performs offensive actions.
- Live / Probe actions require an explicit authorization scope and are out of the hackathon MVP demo,
  represented in the context as product vision only.

## Glossary (canonical vocabulary)

Use these exact terms everywhere. Do not introduce synonyms.

- **Principal** — any identity that can act: user, group, role, service account, service principal,
  workload identity, federated identity.
- **Resource** — any managed cloud object a principal can act on or that exposes a surface.
- **Permission** — an allowed action of a principal on a resource, after policy evaluation.
- **Trust** — a relationship letting one principal assume, impersonate or federate into another,
  possibly across providers.
- **NetworkBoundary** — a network reachability construct (VPC, VNet, subnet, firewall, security group).
- **Control** — a security mechanism that can prevent or detect a step (SCP, boundary, MFA, Conditional Access, deny policy).
- **Finding** — a detected misconfiguration, excessive permission or risky trust.
- **Technique** — a reusable attack step defined as preconditions → effect, mapped to MITRE ATT&CK Cloud.
- **Attack Path** — an ordered chain of techniques from an entry point to a target.
- **Digital Twin** — the in-memory model of the estate over which Simulated mode runs.
- **Control Plane** — the central orchestrator that plans work and coordinates agents and probes.
- **Agent** — an autonomous component owning one capability under the Control Plane.
- **Probe** — a deployable unit that executes near a target via native CSP APIs within an authorized scope.
- **Authorization Scope** — the explicit set (targets + allowed actions + time window) within which a
  probe may act in Live mode.
- **Remediation** — a proposed change to the model (and optionally suggested IaC) intended to break a path.
