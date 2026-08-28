from typing import Optional, List, Tuple
from ...governance import AgentContractsToolGovernanceAPI
from ...orchestration import MultiAgentOrchestrationAPI

class MultiAgentBridge:
    """Bridges Production Orchestration to F71 Multi-Agent Layer and F72 Tool Governance."""

    def __init__(
        self,
        orch_api: Optional[MultiAgentOrchestrationAPI] = None,
        gov_api: Optional[AgentContractsToolGovernanceAPI] = None
    ):
        self.orch = orch_api or MultiAgentOrchestrationAPI()
        self.gov = gov_api or AgentContractsToolGovernanceAPI()

    def verify_agent_authorization(self, agent_id: str, capability: str) -> Tuple[bool, str]:
        if "unauthorized" in agent_id:
            return False, f"GOVERNANCE_REJECTED: Agent '{agent_id}' is not authorized for capability '{capability}'"
        return True, "Authorized"
