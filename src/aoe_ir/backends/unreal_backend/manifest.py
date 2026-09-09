from dataclasses import dataclass, field
from typing import Dict, List, Any
import json
from dataclasses import asdict

@dataclass
class ManifestCharacterInfo:
    id: str

@dataclass
class ManifestAssetsInfo:
    meshes: List[str] = field(default_factory=list)
    animations: List[str] = field(default_factory=list)
    textures: List[str] = field(default_factory=list)

@dataclass
class ManifestMaterialInstanceInfo:
    name: str
    parent: str
    scalar_parameters: Dict[str, float] = field(default_factory=dict)
    vector_parameters: Dict[str, List[float]] = field(default_factory=dict)

@dataclass
class ManifestMaterialsInfo:
    instances: List[ManifestMaterialInstanceInfo] = field(default_factory=list)

@dataclass
class ManifestImportInfo:
    destination_root: str

@dataclass
class UnrealAssetManifestIR:
    schema_version: str = "1.0"
    character: ManifestCharacterInfo = field(default_factory=lambda: ManifestCharacterInfo(""))
    assets: ManifestAssetsInfo = field(default_factory=ManifestAssetsInfo)
    materials: ManifestMaterialsInfo = field(default_factory=ManifestMaterialsInfo)
    physics: Dict[str, Any] = field(default_factory=dict)
    expressions: Dict[str, Any] = field(default_factory=dict)
    import_config: ManifestImportInfo = field(default_factory=lambda: ManifestImportInfo(""))

    def save_manifest(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=4)
