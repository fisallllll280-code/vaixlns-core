from external_integration_gate import ExternalIntegrationGate, IntegrationKind, IntegrationSpec

def make_spec():
    return IntegrationSpec("model:core:test", IntegrationKind.MODEL, "provider://model",
                           ("inference",), "v1", "dep:v1", "env:v1", "vaixlns")

def kwargs(spec, **changes):
    v=dict(allowed_kinds=frozenset({IntegrationKind.MODEL}),
           allowed_capabilities=frozenset({"inference"}),
           proof_identity=spec.identity,
           proof_dependency_fingerprint=spec.dependency_fingerprint,
           proof_environment_fingerprint=spec.environment_fingerprint,
           proof_expires_epoch=200, now_epoch=120, explicit_authority=True)
    v.update(changes); return v

def test_default_denies_without_fresh_proof_and_authority():
    s=make_spec(); d=ExternalIntegrationGate().admit(
        s, **kwargs(s, proof_identity=None, proof_expires_epoch=None, explicit_authority=False))
    assert not d.admitted and "PROOF_NOT_FRESH" in d.reasons

def test_admits_only_when_all_conditions_hold():
    s=make_spec(); assert ExternalIntegrationGate().admit(s, **kwargs(s)).admitted

def test_capability_change_blocks():
    s=make_spec()
    c=IntegrationSpec(**{**s.__dict__,"capabilities":("inference","write")})
    d=ExternalIntegrationGate().admit(c, **kwargs(s))
    assert not d.admitted and "CAPABILITY_FORBIDDEN:write" in d.reasons

def test_dependency_drift_blocks():
    s=make_spec(); d=ExternalIntegrationGate().admit(
        s, **kwargs(s, proof_dependency_fingerprint="dep:v2"))
    assert not d.admitted and "PROOF_DEPENDENCY_MISMATCH" in d.reasons
