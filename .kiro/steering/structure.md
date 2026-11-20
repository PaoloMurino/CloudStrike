---
inclusion: always
---

# CloudStrike — Structure & Module Boundaries

Permanent architecture rules (`ARC-*`) and the repository layout. Terms follow `product.md`.

## Repository layout

```
CloudStrike/
├── src/
│   ├── core/
│   │   ├── model/          # canonical graph: nodes, edges, GraphStore interface (MC-*)
│   │   ├── rules/          # misconfiguration rule engine -> Finding
│   │   ├── paths/          # technique catalog loader + attack-path analysis
│   │   ├── simulation/     # deterministic execution over the digital twin
│   │   └── remediation/    # graph patch, re-simulation, before/after diff
│   ├── agents/             # orchestrator (Control Plane) + specialized agents (AG-*)
│   ├── probes/             # deployable probe runtime + authorization enforcement
│   ├── adapters/
│   │   ├── aws/            # AWS native-API adapter (read + action)
│   │   ├── azure/          # Azure native-API adapter
│   │   └── gcp/            # GCP native-API adapter
│   └── ui/                 # TypeScript/React + Cytoscape.js
├── catalogs/
│   ├── techniques/         # YAML technique definitions (preconditions -> effect)
│   └── controls/           # YAML control definitions per provider
├── datasets/               # synthetic lab snapshots (no real data)
├── tools/context-lint/     # context validator (stdlib only)
└── context-eval/           # behavioral tests + generated traceability matrix
```

## Architecture rules

- **ARC-01 Canonical core.** The graph model is provider-neutral. Provider specifics live in
  namespaced attributes (`aws.*`, `azure.*`, `gcp.*`), never as parallel models (`AD-01`).
- **ARC-02 Ports & adapters.** The dependency direction is one-way: `adapters/* -> core/*`. Core
  MUST NOT import a provider SDK or an adapter. Adding a provider means adding an adapter and MUST
  NOT modify core (`AD-02`, enforced by `QA-07`).
- **ARC-03 Catalogs are external.** `core/paths` and `core/rules` load techniques and controls from
  `catalogs/` at runtime. No technique or control hardcoded in engine code (`AD-05`, `QA-08`).
- **ARC-04 Agents depend on core, not the reverse.** `agents/*` and `probes/*` orchestrate and call
  `core/*` and `adapters/*`. `core/*` MUST NOT import `agents/*` or `probes/*`.
- **ARC-05 Probes isolate action behind authorization.** Any action (non-read) a probe performs via a
  native CSP API MUST pass through the authorization check in `probes/` before reaching an adapter
  (`SEC-04`, `SEC-05`).
- **ARC-06 One capability per module.** Each `core/*` and each specialized agent owns exactly one
  capability from `product.md`. Cross-capability logic goes through defined interfaces, not reach-in.

## Spec ↔ module map

| Spec | Primary modules |
| --- | --- |
| cloud-graph-model | `core/model`, `adapters/*`, `datasets` |
| misconfiguration-detection | `core/rules`, `catalogs/controls` |
| attack-path-analysis | `core/paths`, `catalogs/techniques` |
| attack-simulation | `core/simulation` |
| remediation-whatif | `core/remediation` |
| agent-orchestration | `agents/` |
| probe-lifecycle | `probes/`, `adapters/*` |
| graph-visualization | `src/ui` |
