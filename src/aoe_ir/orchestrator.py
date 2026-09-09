from dataclasses import dataclass, field
from typing import Dict, List, Any
import json
import os
from .character import CharacterIR
from .appearance import AppearanceProfile
from .style_presets import StyleProfile

@dataclass
class CharacterRecipe:
    recipe_id: str
    base_mesh_path: str
    appearance_profile: AppearanceProfile
    style_profile: StyleProfile
    animation_graph: Any = None
    ik_config: Any = None

@dataclass
class ProductionBatchIR:
    batch_id: str
    recipes: List[CharacterRecipe] = field(default_factory=list)
    output_directory: str = "batch_output"

class AssetOrchestrator:
    """Manages multi-character production and automated batching through recipes."""

    def __init__(self, blender_backend, unreal_backend):
        self.blender_backend = blender_backend
        self.unreal_backend = unreal_backend

    def process_batch(self, batch: ProductionBatchIR) -> Dict[str, Any]:
        """
        Executes a full multi-character production run.
        For each recipe, runs through Blender (generation/bake) and Unreal (export/manifest).
        """
        os.makedirs(batch.output_dir, exist_ok=True)
        results = {}

        for recipe in batch.recipes:
            char = CharacterIR(character_id=recipe.recipe_id, appearance=recipe.appearance_profile)
            char.style = recipe.style_profile
            char.metadata["base_mesh"] = recipe.base_mesh_path

            if recipe.animation_graph:
                char.metadata["animation_graph"] = recipe.animation_graph
            if recipe.ik_config:
                char.ik_config = recipe.ik_config

            # 1. Pipeline Execution in Blender (Procedural Gen / Animation Bake)
            blender_result = self.blender_backend.export_asset(char)

            # 2. Pipeline Export to Unreal (Manifests / Zero-Click Script)
            char_output_dir = os.path.join(batch.output_dir, recipe.recipe_id)
            unreal_result = self.unreal_backend.export_asset(char, output_dir=char_output_dir)

            results[recipe.recipe_id] = {
                "blender_status": blender_result["status"],
                "unreal_manifest": unreal_result["manifest_path"]
            }

        return {
            "batch_id": batch.batch_id,
            "status": "COMPLETED",
            "characters_processed": len(batch.recipes),
            "results": results
        }
