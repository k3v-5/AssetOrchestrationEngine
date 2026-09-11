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
            animation_deformation=True,
            native_action_baking=True,
            fbx_animation_export=False
        )

    def export_asset(self, asset: AssetIR, **kwargs) -> Dict[str, Any]:
        self.check_capabilities(asset)

        """Translates the AssetIR to a .blend file using the real Blender Executor if enabled."""

        if self.use_real_executor and self.executor_script:
            from .headless_runner import BlenderHeadlessRunner
            runner = BlenderHeadlessRunner()

            # Serialize the AssetIR to JSON so the blender python script can read it
            asset_dict = _dataclass_to_dict(asset)
            fbx_path = kwargs.get("fbx_path")
            if not fbx_path:
                fbx_path = os.path.join(os.path.dirname(kwargs.get("filepath", "output.blend")), f"{getattr(asset, 'asset_id', getattr(asset, 'character_id', 'Unknown'))}.fbx")

            args = {
                "asset": asset_dict,
                "filepath": kwargs.get("filepath", "output.blend"),
                "fbx_path": fbx_path,
                "render_path": kwargs.get("render_path"),
                "qa_report_path": kwargs.get("qa_report_path", os.path.join(os.path.dirname(kwargs.get("filepath", "output.blend")), f"{getattr(asset, 'asset_id', getattr(asset, 'character_id', 'Unknown'))}_qa_report.json"))
            }

            try:
                result = runner.run_script(self.executor_script, args)
                result["backend"] = self.get_backend_name()
                result["asset_id"] = getattr(asset, "asset_id", getattr(asset, "character_id", "Unknown"))
                return result
            except RuntimeError as e:
                return {"status": "FAILED", "error": str(e)}

        # SIMULATED FBX EXPORT LOGIC FOR HEADLESS BLENDER
        # In a real execution, this would be inside the executor.py running in bpy context.
        # Required for UE5:
        # bpy.ops.export_scene.fbx(
        #     filepath=kwargs.get("fbx_path", "output.fbx"),
        #     axis_forward='-Y',
        #     axis_up='Z',
        #     bake_space_transform=True,
        #     use_mesh_modifiers=True, # Critical for Inverted Hull NPR
        #     mesh_smooth_type='FACE',
        #     object_types={'ARMATURE', 'MESH'},
        #     add_leaf_bones=False
        # )

        # Fallback to simulated plan if real execution is not requested
        result = {
            "status": "SUCCESS (SIMULATED)",
            "backend": self.get_backend_name(),
            "asset_id": getattr(asset, 'asset_id', getattr(asset, 'character_id', 'Unknown')),
            "generated_nodes": self._generate_shader_graph(asset),
            "exported_fbx": kwargs.get("fbx_path", f"{getattr(asset, 'asset_id', getattr(asset, 'character_id', 'Unknown'))}.fbx")
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
