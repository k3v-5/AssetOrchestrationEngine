from abc import ABC, abstractmethod
from ..asset import AssetIR
from ..scene import SceneIR
from typing import Dict, Any

class RenderBackend(ABC):
    """Abstract base class for all render backends (Blender, Unreal, Unity, etc)."""

    @abstractmethod
    def get_backend_name(self) -> str:
        pass

    @abstractmethod
    def export_asset(self, asset: AssetIR) -> Dict[str, Any]:
        """Translates the AssetIR into backend-specific formats/files."""
        pass

    @abstractmethod
    def export_scene(self, scene: SceneIR) -> Dict[str, Any]:
        """Translates a SceneIR into backend-specific scene/level representation."""
        pass
