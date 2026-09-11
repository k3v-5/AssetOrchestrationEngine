from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from .appearance import AppearanceProfile

@dataclass
class GeometryIR:
    mesh_path: str = ""
    vertex_count: int = 0
    triangle_count: int = 0
    uv_channels: int = 1
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SemanticRegionIR:
    region_id: str
    vertex_indices: List[int] = field(default_factory=list)
    face_indices: List[int] = field(default_factory=list)

@dataclass
class RigIR:
    skeleton_type: str = "HUMANOID"
    bone_count: int = 0
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnimationIR:
    clips: List[str] = field(default_factory=list)
    retarget_profile: str = ""
    style_parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AssetIR:
    asset_id: str
    geometry: GeometryIR = field(default_factory=GeometryIR)
    rig: Optional[RigIR] = None
    animation: Optional[AnimationIR] = None
    semantic_regions: Dict[str, SemanticRegionIR] = field(default_factory=dict)
    appearance: AppearanceProfile = field(default_factory=lambda: AppearanceProfile(appearance_id="default"))
    metadata: Dict[str, Any] = field(default_factory=dict)
