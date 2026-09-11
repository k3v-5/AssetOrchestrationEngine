import unittest
import tempfile
import os
from src.aoe_ir.orchestrator import AssetOrchestrator, ProductionBatchIR, CharacterRecipe
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily
from src.aoe_ir.style_presets import StyleProfile, StyleLayerIR
from src.aoe_ir.backends.unreal import UnrealBackend

# Mock backend for Blender so we don't need real headless execution in this unit test
class MockBlenderBackend:
    def export_asset(self, char):
        return {"status": "SUCCESS"}

class TestAssetOrchestrator(unittest.TestCase):
    def test_batch_production(self):
        # Setup Recipes
        app1 = AppearanceProfile(appearance_id="hero_app", family=AppearanceFamily.NPR)
        style1 = StyleProfile()
        recipe1 = CharacterRecipe(recipe_id="Hero_01", base_mesh_path="base_hero.fbx", appearance_profile=app1, style_profile=style1)

        app2 = AppearanceProfile(appearance_id="villain_app", family=AppearanceFamily.PBR)
        style2 = StyleProfile()
        recipe2 = CharacterRecipe(recipe_id="Villain_01", base_mesh_path="base_villain.fbx", appearance_profile=app2, style_profile=style2)

        batch = ProductionBatchIR(batch_id="cinematic_scene_1", recipes=[recipe1, recipe2])

        orchestrator = AssetOrchestrator(blender_backend=MockBlenderBackend(), unreal_backend=UnrealBackend())

        with tempfile.TemporaryDirectory() as tmpdir:
            batch.output_dir = tmpdir
            result = orchestrator.process_batch(batch)

            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(result["characters_processed"], 2)

            # Verify Unreal Output
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "Hero_01", "Hero_01_manifest.json")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "Villain_01", "Villain_01_manifest.json")))

            # Verify Zero-Click scripts
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "Hero_01", "ue5_import_orchestrator.py")))
            self.assertTrue(os.path.exists(os.path.join(tmpdir, "Villain_01", "ue5_import_orchestrator.py")))

if __name__ == '__main__':
    unittest.main()
