from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .asset import AssetIR

@dataclass
class SceneIR:
    scene_id: str
    assets: List[AssetIR] = field(default_factory=list)
    render_settings: Dict[str, Any] = field(default_factory=dict)
    export_settings: Dict[str, Any] = field(default_factory=dict)
