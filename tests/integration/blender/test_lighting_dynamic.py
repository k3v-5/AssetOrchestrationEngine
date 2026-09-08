import unittest
import os
import tempfile
import hashlib
from src.aoe_ir.asset import AssetIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, RimLightProfile
from src.aoe_ir.style_presets import StylePresets
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner

class TestLightingDynamic(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

    def get_file_hash(self, filepath):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def test_toon_shader_reacts_to_light(self):
        # We test that the exact same asset rendered with light in 3 different positions
        # produces 3 different renders.
        # Testing the advanced toon model with rim light reacting dynamically
        app = StylePresets.create_cartoon()
        asset = AssetIR(
            asset_id="MonkeyToonLightTest",
            appearance=app
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            hashes = []
            for i, light_pos in enumerate([(0, 5, 0), (5, 0, 0), (-5, -5, 5)]):
                render_path = os.path.join(tmpdir, f"render_light_{i}.png")

                # We inject a special instruction into the dict to move the light just for this test
                # We'll need to pass it to the executor. We can use the 'parameters' field in the asset or scene
                asset.metadata["test_light_loc"] = light_pos

                self.backend.export_asset(asset, render_path=render_path)

                self.assertTrue(os.path.exists(render_path))
                hashes.append(self.get_file_hash(render_path))

            # The renders must be different if the shader truly reacts to light
            self.assertNotEqual(hashes[0], hashes[1])
            self.assertNotEqual(hashes[1], hashes[2])
            self.assertNotEqual(hashes[0], hashes[2])

if __name__ == "__main__":
    unittest.main()
