from typing import Dict, Any, List, Optional
from ..core.orchestrator_types import AgentType, TaskState, LockType, ExecutionMode, RiskLevel
from ..core.orchestrator_schema import (
    AgentDefinition, Task, Checkpoint, ExecutionReport, OrchestratorConfig, OrchestrationCorrectionPlan
)
from ..execution.ai_orchestrator import AIOrchestrator

class BuildOrchestratorAPI:
    """
    Build Orchestrator Public API (AOE v30)
    """
    def __init__(self, config: Optional[OrchestratorConfig] = None):
        self.orchestrator = AIOrchestrator(config)

    def run_orchestrated_build(
        self,
        asset_id: str,
        initial_parameters: Dict[str, Any],
        simulated_qa_error: Optional[str] = None
    ) -> ExecutionReport:
        return self.orchestrator.execute_asset_build(
            asset_id=asset_id,
            initial_parameters=initial_parameters,
            simulated_qa_error=simulated_qa_error
        )

    def validate_tool_permission(self, agent_id: str, tool_name: str) -> bool:
        return self.orchestrator.registry.validate_tool_permission(agent_id, tool_name)
