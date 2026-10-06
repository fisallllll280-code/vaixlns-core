"""VAIXLNS Core portable external integration gate.

The module uses only the standard library so it remains usable as a low-level
constitutional boundary even when the higher runtime stack is unavailable.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class IntegrationKind(str, Enum):
    MODEL = "MODEL"
    API = "API"
    SERVER = "SERVER"
    TOOL = "TOOL"
    CONNECTOR = "CONNECTOR"
    REPOSITORY = "REPOSITORY"
    DATA_SOURCE = "DATA_SOURCE"


@dataclass(frozen=True)
class IntegrationSpec:
    identity: str
    kind: IntegrationKind
    endpoint: str
    capabilities: tuple[str, ...]
    contract_version: str
    dependency_fingerprint: str
    environment_fingerprint: str
    owner: str


@dataclass(frozen=True)
class GateDecision:
    admitted: bool
    state: str
    reasons: tuple[str, ...]


class ExternalIntegrationGate:
    """Default deny plus explicit proof/authority requirements."""

    def admit(
        self,
        spec: IntegrationSpec,
        *,
        allowed_kinds: frozenset[IntegrationKind],
        allowed_capabilities: frozenset[str],
        proof_fresh: bool,
        proof_bound_identity: str | None,
        explicit_authority: bool,
        forbidden_endpoints: frozenset[str] = frozenset(),
    ) -> GateDecision:
        reasons: list[str] = []
        if spec.kind not in allowed_kinds:
            reasons.append("KIND_FORBIDDEN")
        if spec.endpoint in forbidden_endpoints:
            reasons.append("ENDPOINT_FORBIDDEN")
        if not spec.owner:
            reasons.append("OWNER_MISSING")
        if not spec.contract_version:
            reasons.append("CONTRACT_MISSING")
        if not spec.dependency_fingerprint:
            reasons.append("DEPENDENCY_FINGERPRINT_MISSING")
        if not spec.environment_fingerprint:
            reasons.append("ENVIRONMENT_FINGERPRINT_MISSING")
        unauthorized = sorted(set(spec.capabilities) - set(allowed_capabilities))
        reasons.extend(f"CAPABILITY_FORBIDDEN:{c}" for c in unauthorized)
        if not proof_fresh:
            reasons.append("PROOF_NOT_FRESH")
        if proof_bound_identity != spec.identity:
            reasons.append("PROOF_IDENTITY_MISMATCH")
        if not explicit_authority:
            reasons.append("EXPLICIT_AUTHORITY_REQUIRED")
        return GateDecision(
            admitted=not reasons,
            state="ADMITTED" if not reasons else "QUARANTINED",
            reasons=("ADMITTED",) if not reasons else tuple(reasons),
        )
