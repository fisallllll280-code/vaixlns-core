# VAIXLNS — Sovereign Constitutional Computing Fabric

**v0.1: Vertical Slice — Full Closed Loop**

A programmable constitutional substrate for verified computation that transforms:

```
INTENT → V-IR → VERIFY → PROOF → CAPABILITY → LEASE → VX → EVIDENCE → LEDGER → REPLAY → IDENTICAL STATE
```

## Status: IMPLEMENTED + TESTED

Every component is working, tested, and observable.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Run the system
python -m vaixlns.api.server

# Access API
curl http://localhost:8000/health
```

## Architecture

```
VAIXLNS/
├── vx/                    # Runtime core (evolved from vx_system.py)
│   ├── runtime/           # VX execution engine
│   ├── state/             # State machine & closure verification
│   ├── events/            # Event store & ledger
│   ├── replay/            # Deterministic replay engine
│   └── execution/         # Execution context
├── vir/                   # V-IR semantic representation
│   ├── intent.py          # Intent graph
│   ├── contract.py        # Contract definitions
│   ├── policy.py          # Policy graph
│   └── capability.py      # Capability graph
├── verifier/              # CVL verification layer
│   ├── determinism.py     # Determinism verification
│   ├── replay.py          # Replay integrity
│   ├── ledger.py          # Ledger hash chain
│   ├── closure.py         # Proof closure
│   └── result.py          # VerificationResult
├── governance/            # Policy & authorization
│   ├── policy.py          # Policy engine
│   ├── lease.py           # Proof lease management
│   └── capability.py      # Capability registry
├── evidence/              # Evidence collection
├── ledger/                # Event ledger
├── api/                   # REST API
├── tests/                 # Full test suite
├── examples/              # Working examples
├── specs/                 # Formal specifications
└── docs/                  # Architecture documentation
```

## Invariants (ENFORCED)

- ✅ I1:  No Unverified Execution
- ✅ I2:  No Orphan State
- ✅ I3:  No Untracked Mutation
- ✅ I4:  No Invalid Lease
- ✅ I5:  No Unauthorized Capability
- ✅ I6:  No Broken Lineage
- ✅ I7:  No Invalid Replay
- ✅ I8:  No Silent Failure
- ✅ I9:  No Unproven Guarantee
- ✅ I10: No Policy Bypass
- ✅ I11: No Hidden External Effect
- ✅ I12: No Unbounded Evolution

## Tests

- Unit tests for each component
- Integration tests for full cycle
- Determinism verification
- Replay fidelity tests
- Ledger integrity tests
- Orphan state detection
- Policy enforcement
- Lease expiration
- Capability binding
- Proof closure validation

## Grand Demo

```bash
python examples/grand_demo.py
```

Shows complete cycle from Intent → Replay with:
- Automatic capability discovery
- Policy validation
- Proof generation
- Evidence collection
- Ledger recording
- Deterministic replay

## API Endpoints

```
POST   /intent              # Submit intent
POST   /verify              # Verify intent
GET    /execution/{id}      # Get execution state
GET    /events              # List events
GET    /state/{id}          # Get state snapshot
POST   /replay              # Replay from checkpoint
GET    /capabilities        # List capabilities
GET    /proof/{id}          # Get proof
GET    /evidence/{id}       # Get evidence
GET    /ledger/integrity    # Verify ledger chain
```

## Philosophy

No unverified claims. Every module is IMPLEMENTED, TESTED, OBSERVABLE.

- V defines Intent
- V-IR defines Meaning
- Verifier establishes Assurance
- Governance establishes Authority
- VX executes
- Evidence proves what happened
- Ledger records Truth
- Replay reconstructs Truth

## Next Phases

- v0.2: V Language Parser + Compiler
- v0.3: V-CAP Federation
- v0.4: OIF Placement Optimization
- v0.5: Intelligence Fabric
- v0.6: Pattern Forest
- v0.7: Innovation Engine
- v1.0: Full VAIXLNS Sovereign Fabric

---

**Built to prove intent, not promise dreams.** 🔥
