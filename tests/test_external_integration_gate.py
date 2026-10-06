from external_integration_gate import ExternalIntegrationGate, IntegrationKind, IntegrationSpec


def make_spec() -> IntegrationSpec:
    return IntegrationSpec(
        identity="model:core:test",
        kind=IntegrationKind.MODEL,
        endpoint="provider://model",
        capabilities=("inference",),
        contract_version="v1",
        dependency_fingerprint="dep:v1",
        environment_fingerprint="env:v1",
        owner="vaixlns",
    )


def test_default_denies_without_fresh_proof_and_authority():
    d = ExternalIntegrationGate().admit(
        make_spec(),
        allowed_kinds=frozenset({IntegrationKind.MODEL}),
        allowed_capabilities=frozenset({"inference"}),
        proof_fresh=False,
        proof_bound_identity=None,
        explicit_authority=False,
    )
    assert d.admitted is False
    assert "PROOF_NOT_FRESH" in d.reasons


def test_admits_only_when_all_boundary_conditions_hold():
    spec = make_spec()
    d = ExternalIntegrationGate().admit(
        spec,
        allowed_kinds=frozenset({IntegrationKind.MODEL}),
        allowed_capabilities=frozenset({"inference"}),
        proof_fresh=True,
        proof_bound_identity=spec.identity,
        explicit_authority=True,
    )
    assert d.admitted is True


def test_identity_or_capability_change_blocks():
    spec = make_spec()
    d = ExternalIntegrationGate().admit(
        IntegrationSpec(**{**spec.__dict__, "capabilities": ("inference", "write")}),
        allowed_kinds=frozenset({IntegrationKind.MODEL}),
        allowed_capabilities=frozenset({"inference"}),
        proof_fresh=True,
        proof_bound_identity=spec.identity,
        explicit_authority=True,
    )
    assert d.admitted is False
    assert "CAPABILITY_FORBIDDEN:write" in d.reasons
