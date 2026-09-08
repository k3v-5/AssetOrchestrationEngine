from .base import RenderBackend
from ..asset import AssetIR
from ..scene import SceneIR
from typing import Dict, Any
from ..appearance import AppearanceFamily, ShaderModel

class BlenderBackend(RenderBackend):
    def get_backend_name(self) -> str:
        return "BLENDER_RUNTIME"

    def export_asset(self, asset: AssetIR) -> Dict[str, Any]:
        """Translates the AssetIR to a .blend file equivalent representation."""
        result = {
            "status": "SUCCESS",
            "backend": self.get_backend_name(),
            "asset_id": asset.asset_id,
            "generated_nodes": self._generate_shader_graph(asset)
        }
        return result

    def export_scene(self, scene: SceneIR) -> Dict[str, Any]:
        return {"status": "SUCCESS", "scene_id": scene.scene_id}

    def _generate_shader_graph(self, asset: AssetIR) -> Dict[str, Any]:
        """Maps the abstract AppearanceProfile into Blender Node setups."""
        app = asset.appearance
        nodes = {}

        if app.family == AppearanceFamily.PBR:
            nodes["PBR_OUTPUT"] = "Principled BSDF"
        elif app.family == AppearanceFamily.NPR:
            if app.style.shading.model == ShaderModel.TOON:
                nodes["TOON_RAMP"] = "ColorRamp (Constant)"
                nodes["TOON_BANDS"] = app.style.shading.band_count
                if app.style.outline.enabled:
                    nodes["OUTLINE"] = app.style.outline.method.value

        return nodes
