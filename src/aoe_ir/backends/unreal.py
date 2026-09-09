from .base import RenderBackend, BackendCapabilities
from ..asset import AssetIR
from ..scene import SceneIR
from typing import Dict, Any
from ..appearance import AppearanceFamily, ShaderModel
import os
from .unreal_backend.unreal_exporter import UnrealExporter

class UnrealBackend(RenderBackend):
    def get_backend_name(self) -> str:
        return "UNREAL_ENGINE_5"

    def get_capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            pbr=True,
            toon=True,
            inverted_hull=False,
            semantic_overrides=True,
            stencil=True,
            post_process_outline=True,
            animation_deformation=True,
            native_action_baking=False,
            fbx_animation_export=True
        )

    def export_asset(self, asset: AssetIR, **kwargs) -> Dict[str, Any]:
        self.check_capabilities(asset)
        output_dir = kwargs.get("output_dir", "unreal_export")
        manifest_path = UnrealExporter(output_dir).export(asset)

        result = {
            "status": "SUCCESS",
            "backend": self.get_backend_name(),
            "asset_id": getattr(asset, "character_id", getattr(asset, "asset_id", "Unknown")),
            "manifest_path": manifest_path
        }
        return result

    def export_scene(self, scene: SceneIR, **kwargs) -> Dict[str, Any]:
        return {"status": "SUCCESS", "scene_id": scene.scene_id}

    def _resolve_master_material(self, asset: AssetIR) -> str:
        app = asset.appearance
        if app.family == AppearanceFamily.PBR:
            return "/Engine/MasterMaterials/M_PBR_Master"
        elif app.family == AppearanceFamily.NPR:
            if app.style.shading.model == ShaderModel.TOON:
                return "/Engine/MasterMaterials/M_NPR_Anime_Master"
            elif app.style.shading.model == ShaderModel.UNLIT:
                return "/Engine/MasterMaterials/M_Unlit_Master"
        return "/Engine/MasterMaterials/M_Default"
