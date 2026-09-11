from abc import ABC, abstractmethod
from ..asset import AssetIR
from ..scene import SceneIR
from typing import Dict, Any
from dataclasses import dataclass, field

@dataclass
class BackendCapabilities:
    pbr: bool = False
    toon: bool = False
    inverted_hull: bool = False
    semantic_overrides: bool = False
    stencil: bool = False
    post_process_outline: bool = False
    animation_deformation: bool = False
    native_action_baking: bool = False # e.g. Blender bpy.data.actions
    fbx_animation_export: bool = False # e.g. Unreal requirements

class BackendCapabilityError(Exception):
    def __init__(self, required_capability: str, backend: str, reason: str):
        self.required_capability = required_capability
        self.backend = backend
        self.reason = reason
        super().__init__(f"BackendCapabilityError: '{backend}' lacks required capability '{required_capability}'. Reason: {reason}")

class RenderBackend(ABC):
    """Abstract base class for all render backends (Blender, Unreal, Unity, etc)."""

    @abstractmethod
    def get_backend_name(self) -> str:
        pass

    @abstractmethod
    def get_capabilities(self) -> BackendCapabilities:
        pass

    def check_capabilities(self, asset: AssetIR) -> None:
        caps = self.get_capabilities()
        app = asset.appearance

        # Check families
        if "NPR" in str(app.family):
            if "TOON" in str(app.style.shading.model) and not caps.toon:
                raise BackendCapabilityError("toon", self.get_backend_name(), "Backend does not support NPR Toon Shading.")

            # Check outlines
            if app.style.outline.enabled:
                method_str = str(app.style.outline.method)
                if "INVERTED_HULL" in method_str and not caps.inverted_hull:
                    raise BackendCapabilityError("inverted_hull", self.get_backend_name(), "Backend does not support Inverted Hull outlines.")
                if "POST_PROCESS" in method_str and not caps.post_process_outline:
                    raise BackendCapabilityError("post_process_outline", self.get_backend_name(), "Backend does not support Post-Process outlines.")

        elif "PBR" in str(app.family):
            if not caps.pbr:
                raise BackendCapabilityError("pbr", self.get_backend_name(), "Backend does not support PBR rendering.")

        # Check semantic overrides
        if getattr(app, "region_overrides", None) and not caps.semantic_overrides:
            raise BackendCapabilityError("semantic_overrides", self.get_backend_name(), "Backend does not support Semantic Region Overrides.")

    @abstractmethod
    def export_asset(self, asset: AssetIR, **kwargs) -> Dict[str, Any]:
        """Translates the AssetIR into backend-specific formats/files."""
        pass

    @abstractmethod
    def export_scene(self, scene: SceneIR, **kwargs) -> Dict[str, Any]:
        """Translates a SceneIR into backend-specific scene/level representation."""
        pass
