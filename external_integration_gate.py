"""VAIXLNS Core portable external integration gate."""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

class IntegrationKind(str, Enum):
    MODEL="MODEL"; API="API"; SERVER="SERVER"; TOOL="TOOL"
    CONNECTOR="CONNECTOR"; REPOSITORY="REPOSITORY"; DATA_SOURCE="DATA_SOURCE"

@dataclass(frozen=True)
class IntegrationSpec:
    identity:str; kind:IntegrationKind; endpoint:str; capabilities:tuple[str,...]
    contract_version:str; dependency_fingerprint:str; environment_fingerprint:str; owner:str

@dataclass(frozen=True)
class GateDecision:
    admitted:bool; state:str; reasons:tuple[str,...]

class ExternalIntegrationGate:
    """Default deny; admission requires identity-bound, fresh proof and authority."""
    def admit(self,spec:IntegrationSpec,*,allowed_kinds:frozenset[IntegrationKind],
              allowed_capabilities:frozenset[str],proof_identity:str|None,
              proof_dependency_fingerprint:str|None,proof_environment_fingerprint:str|None,
              proof_expires_epoch:int|None,now_epoch:int,explicit_authority:bool,
              forbidden_endpoints:frozenset[str]=frozenset()) -> GateDecision:
        reasons=[]
        if spec.kind not in allowed_kinds: reasons.append("KIND_FORBIDDEN")
        if spec.endpoint in forbidden_endpoints: reasons.append("ENDPOINT_FORBIDDEN")
        if not spec.owner: reasons.append("OWNER_MISSING")
        if not spec.contract_version: reasons.append("CONTRACT_MISSING")
        if not spec.dependency_fingerprint: reasons.append("DEPENDENCY_FINGERPRINT_MISSING")
        if not spec.environment_fingerprint: reasons.append("ENVIRONMENT_FINGERPRINT_MISSING")
        reasons += [f"CAPABILITY_FORBIDDEN:{c}" for c in sorted(set(spec.capabilities)-set(allowed_capabilities))]
        if proof_identity != spec.identity: reasons.append("PROOF_IDENTITY_MISMATCH")
        if proof_dependency_fingerprint != spec.dependency_fingerprint: reasons.append("PROOF_DEPENDENCY_MISMATCH")
        if proof_environment_fingerprint != spec.environment_fingerprint: reasons.append("PROOF_ENVIRONMENT_MISMATCH")
        if proof_expires_epoch is None or now_epoch >= proof_expires_epoch: reasons.append("PROOF_NOT_FRESH")
        if not explicit_authority: reasons.append("EXPLICIT_AUTHORITY_REQUIRED")
        return GateDecision(not reasons, "ADMITTED" if not reasons else "QUARANTINED",
                            ("ADMITTED",) if not reasons else tuple(reasons))
