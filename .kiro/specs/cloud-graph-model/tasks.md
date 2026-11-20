# Cloud Graph Model — Tasks

- [ ] 1. Define canonical node/edge dataclasses with namespaced `ns` attributes and `evidence`.
  _Requirements: REQ-GRAPH-01, REQ-GRAPH-02, REQ-GRAPH-05_

- [ ] 2. Implement `GraphStore` interface and `InMemoryGraphStore`.
  _Requirements: REQ-GRAPH-01_

- [ ] 3. Implement deterministic, snapshot-scoped build with stable ordering and a graph hash.
  _Requirements: REQ-GRAPH-06_

- [ ] 4. Implement `SecretRef` and redaction on ingestion and serialization.
  _Requirements: REQ-GRAPH-07_

- [ ] 5. Implement read-only AWS/Azure/GCP ingestion adapters via native SDKs, keeping core SDK-free.
  _Requirements: REQ-GRAPH-03_

- [ ] 6. Emit cross-cloud CAN_ASSUME/TRUSTS edges with the `federation` attribute.
  _Requirements: REQ-GRAPH-04_

- [ ] 7. Tests: determinism hash, import-boundary (no provider SDK in core), no-secret-in-snapshot.
  _Requirements: REQ-GRAPH-03, REQ-GRAPH-06, REQ-GRAPH-07_
