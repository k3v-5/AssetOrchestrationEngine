from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class BoneIR:
    name: str
    head: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    tail: Tuple[float, float, float] = (0.0, 0.0, 1.0)
    roll: float = 0.0
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)

@dataclass
class SkeletonIR:
    skeleton_id: str
    bones: Dict[str, BoneIR] = field(default_factory=dict)
    root_bone: str = "root"

@dataclass
class VertexWeightIR:
    vertex_index: int
    weights: Dict[str, float] = field(default_factory=dict) # bone_name -> weight

@dataclass
class SkinningIR:
    skinning_id: str
    vertex_weights: List[VertexWeightIR] = field(default_factory=list)
    max_influences: int = 4
