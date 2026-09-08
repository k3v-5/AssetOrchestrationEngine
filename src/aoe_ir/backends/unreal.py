from .base import RenderBackend
from ..asset import AssetIR
from ..scene import SceneIR
from typing import Dict, Any
from ..appearance import AppearanceFamily, ShaderModel

class UnrealBackend(RenderBackend):
    def get_backend_name(self) -> str:
        return "UNREAL_ENGINE_5"

    def export_asset(self, asset: AssetIR) -> Dict[str, Any]:
        """Translates the AssetIR to a .uasset / Material Instance representation."""
        result = {
            "status": "SUCCESS",
            "backend": self.get_backend_name(),
            "asset_id": asset.asset_id,
            "master_material": self._resolve_master_material(asset)
        }
        return result

    def export_scene(self, scene: SceneIR) -> Dict[str, Any]:
        return {"status": "SUCCESS", "scene_id": scene.scene_id}

    def _resolve_master_material(self, asset: AssetIR) -> str:
        """Resolves the correct Unreal Master Material based on the AppearanceProfile."""
        app = asset.appearance

        if app.family == AppearanceFamily.PBR:
            return "/Engine/MasterMaterials/M_PBR_Master"
        elif app.family == AppearanceFamily.NPR:
            if app.style.shading.model == ShaderModel.TOON:
                return "/Engine/MasterMaterials/M_NPR_Anime_Master"
            elif app.style.shading.model == ShaderModel.UNLIT:
                return "/Engine/MasterMaterials/M_Unlit_Master"

        return "/Engine/MasterMaterials/M_Default"
