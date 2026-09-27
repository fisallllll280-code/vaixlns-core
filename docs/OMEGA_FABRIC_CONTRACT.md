# Ω∞ Fabric Contract — vaixlns-core

This repository is the semantic/invariant layer of the VAIXLNS federation.

Required invariants:

- authorization precedes execution;
- unverified execution is rejected or quarantined;
- every mutation is ledger-addressable;
- state requires origin, lineage, owner and proof reference;
- replay reconstructs deterministic state;
- evolution requires simulation, verification and governance approval.

Conformance: SPECIFIED until independent runtime evidence is attached.
