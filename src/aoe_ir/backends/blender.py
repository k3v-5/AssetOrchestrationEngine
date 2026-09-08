import os
import dataclasses
import json
from .base import RenderBackend, BackendCapabilities
from ..asset import AssetIR
from ..scene import SceneIR
from typing import Dict, Any, Optional

def _dataclass_to_dict(obj):
    if dataclasses.is_dataclass(obj):
        return {k: _dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    elif isinstance(obj, list):
        return [_dataclass_to_dict(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, 'value'): # Handle Enums
        return obj.value
    else:
        return obj

class BlenderBackend(RenderBackend):
    def __init__(self, use_real_executor: bool = False, executor_script: Optional[str] = None):
        self.use_real_executor = use_real_executor
        self.executor_script = executor_script

    def get_backend_name(self) -> str:
        return "BLENDER_RUNTIME"

    def get_capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            pbr=True,
            toon=True,
            inverted_hull=True,
            semantic_overrides=True,
            stencil=False,
            post_process_outline=False,  # Not implemented in executor yet
            animation_deformation=True
        )

    def export_asset(self, asset: AssetIR, **kwargs) -> Dict[str, Any]:
        self.check_capabilities(asset)

        """Translates the AssetIR to a .blend file using the real Blender Executor if enabled."""

        if self.use_real_executor and self.executor_script:
            from .headless_runner import BlenderHeadlessRunner
            runner = BlenderHeadlessRunner()

            # Serialize the AssetIR to JSON so the blender python script can read it
            asset_dict = _dataclass_to_dict(asset)
            args = {
                "asset": asset_dict,
                "filepath": kwargs.get("filepath", "output.blend"),
                "render_path": kwargs.get("render_path")
            }

            try:
                result = runner.run_script(self.executor_script, args)
                result["backend"] = self.get_backend_name()
                result["asset_id"] = getattr(asset, "asset_id", getattr(asset, "character_id", "Unknown"))
                return result
            except RuntimeError as e:
                return {"status": "FAILED", "error": str(e)}

        # Fallback to simulated plan if real execution is not requested
        result = {
            "status": "SUCCESS (SIMULATED)",
            "backend": self.get_backend_name(),
            "asset_id": asset.asset_id,
            "generated_nodes": self._generate_shader_graph(asset)
        }
        return result

    def export_scene(self, scene: SceneIR, **kwargs) -> Dict[str, Any]:
        return {"status": "SUCCESS (SIMULATED)", "scene_id": scene.scene_id}

    def _generate_shader_graph(self, asset: AssetIR) -> Dict[str, Any]:
        """Simulated shader graph for quick plan inspection"""
        from ..appearance import AppearanceFamily, ShaderModel
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
