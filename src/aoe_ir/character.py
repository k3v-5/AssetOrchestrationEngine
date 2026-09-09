from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from .appearance import AppearanceProfile
from typing import List

@dataclass
class LODConfigIR:
    levels: List[int] = field(default_factory=lambda: [50, 25, 10])
    keep_inverted_hull: List[bool] = field(default_factory=lambda: [True, False, False])

@dataclass
class QALimitsIR:
    max_triangles: int = 50000
    max_bones: int = 100
    max_texture_res: int = 4096

from .skeleton import SkeletonIR, SkinningIR
from .animation import AnimationFoundationIR
from .ik import IKSolverConfigIR
from .facial import FaceRigIR
from .physics import PhysicsRigIR

class SemanticRegionTag(str, Enum):
    # Head Hierarchy
    HEAD = "HEAD"
    FACE = "FACE"
    EYES = "EYES"
    EYEBROWS = "EYEBROWS"
    MOUTH = "MOUTH"
    HAIR = "HAIR"
    EARS = "EARS"

    # Body Hierarchy
    BODY = "BODY"
    SKIN = "SKIN"
    CLOTHING = "CLOTHING"
    SHOES = "SHOES"
    HANDS = "HANDS"
    ACCESSORIES = "ACCESSORIES"

@dataclass
class CharacterSemanticRegionIR:
    region_id: SemanticRegionTag
    mesh_id: str
    vertex_indices: List[int] = field(default_factory=list)

@dataclass
class CharacterMeshIR:
    mesh_id: str
    vertex_count: int = 0
    triangle_count: int = 0
    # Other mesh abstract details

@dataclass
class CharacterIR:
    character_id: str
    meshes: Dict[str, CharacterMeshIR] = field(default_factory=dict)
    skeleton: Optional[SkeletonIR] = None
    skinning: Dict[str, SkinningIR] = field(default_factory=dict) # mesh_id -> SkinningIR
    semantic_regions: List[CharacterSemanticRegionIR] = field(default_factory=list)
    appearance: Optional[AppearanceProfile] = None
    animation: Optional[AnimationFoundationIR] = None
    ik_config: Optional[IKSolverConfigIR] = None
    face_rig: Optional[FaceRigIR] = None
    physics_rig: Optional[PhysicsRigIR] = None
    lod_config: Optional[LODConfigIR] = None
    qa_limits: Optional[QALimitsIR] = None
    metadata: Dict[str, str] = field(default_factory=dict)
