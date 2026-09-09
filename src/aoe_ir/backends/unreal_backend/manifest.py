from dataclasses import dataclass, field
from typing import Dict, List, Any
import json
from dataclasses import asdict

@dataclass
class UnrealAssetManifestIR:
    manifest_id: str
    target_content_path: str = "/Game/AOE"
    source_files: Dict[str, str] = field(default_factory=dict)
    material_instances: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def save_manifest(self, filepath: str):
        with open(filepath, 'w') as f:
            json.dump(asdict(self), f, indent=4)
