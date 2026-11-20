# Attack Path Analysis — Requirements

Spec code: **PATHS**. Loads a data-driven technique catalog and computes ranked, explainable attack
paths over the graph.

## Governing rules

Implements `AD-05`, `AD-06`, `AD-08`, `ARC-03`, `MC-01`, `MC-03`, `MC-04`, `QA-01`, `QA-03`, `QA-04`,
`QA-08`, `SEC-02`. Terms per the `product.md` glossary.

## Requirements

#### REQ-PATHS-01 — Data-driven technique catalog
WHEN the analyzer starts THE SYSTEM SHALL load techniques from `catalogs/techniques/` as data, AND
adding a technique SHALL NOT require changing engine code.

#### REQ-PATHS-02 — Technique schema
WHEN a technique is loaded THE SYSTEM SHALL validate it has preconditions, an effect (the edge/state
it produces) and a MITRE ATT&CK Cloud mapping, and SHALL reject a technique missing any of these.

#### REQ-PATHS-03 — Precondition matching on the graph
WHEN computing paths THE SYSTEM SHALL consider a technique applicable only where its preconditions
match actual graph nodes/edges, citing the matched evidence.

#### REQ-PATHS-04 — Cross-cloud path composition
WHEN techniques chain across providers via CAN_ASSUME/TRUSTS edges THE SYSTEM SHALL compose them
into a single path spanning providers.

#### REQ-PATHS-05 — Explicit risk scoring
WHEN a path is produced THE SYSTEM SHALL score it as risk = likelihood × impact using the documented
formula below, and SHALL attach the factors that produced the score.

#### REQ-PATHS-06 — Deterministic ranking
WHEN the same graph and catalog are analyzed THE SYSTEM SHALL return the same paths in the same
ranked order.

#### REQ-PATHS-07 — No live action
WHEN analyzing paths THE SYSTEM SHALL operate only on the graph model and SHALL NOT perform any
action against a cloud.

## Scoring formula (QA-04)

`risk = likelihood × impact`, both in [0,1].
- `likelihood` = product of per-step feasibility factors (precondition certainty, whether a Control
  on the step is enforcing), clamped to [0,1].
- `impact` = normalized blast radius of the target node (privilege level + number of reachable
  sensitive resources).
A path's factors are stored alongside the score for explainability (`QA-03`).
