# Cloud Graph Model — Design

Implements the requirements in `requirements.md`. Rules cited by ID (see `multicloud-model.md`,
`structure.md`).

## Modules

- `core/model/nodes.py`, `edges.py` — canonical node/edge dataclasses; provider fields live in a
  `ns` attribute dict keyed `aws|azure|gcp` (`REQ-GRAPH-02`).
- `core/model/store.py` — `GraphStore` interface + `InMemoryGraphStore` (MVP). Backend swappable.
- `core/model/snapshot.py` — point-in-time snapshot container, deterministic ordering (`REQ-GRAPH-06`).
- `adapters/{aws,azure,gcp}/ingest.py` — read-only ingestion via native SDKs, mapping to canonical
  nodes/edges (`REQ-GRAPH-03`). Only adapters import provider SDKs (`QA-07`).

## Key decisions

- **Edge provenance** (`REQ-GRAPH-05`): every edge carries `evidence` (source object id + the rule
  that justifies it). Findings and paths reuse this, never re-derive it.
- **Cross-cloud trust** (`REQ-GRAPH-04`): adapters emit CAN_ASSUME/TRUSTS with a `federation`
  attribute (`oidc`, `wif`, `federated-credential`, `stored-secret`). The core treats them uniformly.
- **Secret handling** (`REQ-GRAPH-07`): a `SecretRef(id, location)` type replaces any secret value
  before it reaches the store.
- **Determinism** (`REQ-GRAPH-06`): nodes/edges sorted by stable canonical id before emit; no
  wall-clock or set iteration order in output.

## Properties to test

- Same snapshot → identical graph (hash of sorted node/edge ids).
- No provider SDK import reachable from `core/*` (import-boundary test, `QA-07`).
- No raw secret string present in any serialized snapshot.
