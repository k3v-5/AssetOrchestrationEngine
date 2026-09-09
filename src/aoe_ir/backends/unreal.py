from .base import RenderBackend, BackendCapabilities
from ..asset import AssetIR
from ..scene import SceneIR
from typing import Dict, Any
from ..appearance import AppearanceFamily, ShaderModel

class UnrealBackend(RenderBackend):
    def get_backend_name(self) -> str:
        return "UNREAL_ENGINE_5"

    def get_capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            pbr=True,
            toon=True,
            inverted_hull=False, # Unreal usually does post-process outline
            semantic_overrides=True,
            stencil=True,
            post_process_outline=True,
            animation_deformation=True,
            native_action_baking=False,
            fbx_animation_export=True
        )

    def export_asset(self, asset: AssetIR, **kwargs) -> Dict[str, Any]:
        self.check_capabilities(asset)
        """Translates the AssetIR to a .uasset / Material Instance representation."""
        result = {
            "status": "SUCCESS",
            "backend": self.get_backend_name(),
            "asset_id": asset.asset_id,
            "master_material": self._resolve_master_material(asset)
        }
        return result

    def export_scene(self, scene: SceneIR, **kwargs) -> Dict[str, Any]:
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
