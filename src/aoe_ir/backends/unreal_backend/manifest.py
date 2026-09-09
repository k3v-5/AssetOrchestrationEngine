from dataclasses import dataclass, field
from typing import Dict, List, Any
import json
from dataclasses import asdict

@dataclass
class ManifestMaterialInstanceInfo:
    name: str
    parent: str
    scalar_parameters: Dict[str, float] = field(default_factory=dict)
    vector_parameters: Dict[str, List[float]] = field(default_factory=dict)
    base_textures: Dict[str, str] = field(default_factory=dict)

@dataclass
class PhysicsNodeInfo:
    bone_target: str
    physics_type: str # 'KawaiiPhysics' or 'AnimDynamics'
    stiffness: float = 0.5
    damping: float = 0.2

@dataclass
class MorphTargetInfo:
    name: str
    time: float = 0.0
    value: float = 1.0

@dataclass
class UnrealAssetManifestIR:
    manifest_id: str = "Unknown"
    source_fbx_path: str = ""
    materials_config: List[ManifestMaterialInstanceInfo] = field(default_factory=list)
    physics_nodes: List[PhysicsNodeInfo] = field(default_factory=list)
    morph_targets: List[MorphTargetInfo] = field(default_factory=list)
    destination_root: str = "/Game/AOE_Imports"

    def save_manifest(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=4)
