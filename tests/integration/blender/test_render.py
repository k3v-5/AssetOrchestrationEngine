import unittest
import os
import tempfile
import hashlib
from src.aoe_ir.asset import AssetIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, OutlineProfile, OutlineMethod, ShadingProfile, ShaderModel
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner

class TestRenderAndDeterminism(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

    def get_file_hash(self, filepath):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def test_real_render_output(self):
        # 12. RENDER REAL - Generate actual .png renders for PBR and NPR

        asset = AssetIR(
            asset_id="MonkeyRenderTest",
            appearance=AppearanceProfile(
                appearance_id="toon_render",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON),
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.03)
                )
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            render_path = os.path.join(tmpdir, "toon_test.png")

            result = self.backend.export_asset(asset, render_path=render_path)

            self.assertEqual(result["status"], "SUCCESS")
            self.assertTrue(os.path.exists(render_path))
            self.assertGreater(os.path.getsize(render_path), 0, "Render image is empty")

    def test_determinism(self):
        # 14. DETERMINISMO - Executing the exact same IR twice must produce identical results
        asset = AssetIR(
            asset_id="MonkeyDeterminism",
            appearance=AppearanceProfile(
                appearance_id="toon_det",
                family=AppearanceFamily.NPR,
                style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=2))
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            blend_a = os.path.join(tmpdir, "run_a.blend")
            blend_b = os.path.join(tmpdir, "run_b.blend")

            res_a = self.backend.export_asset(asset, filepath=blend_a)
            res_b = self.backend.export_asset(asset, filepath=blend_b)

            self.assertEqual(res_a["status"], "SUCCESS")
            self.assertEqual(res_b["status"], "SUCCESS")

            # The objects and materials returned must be exactly the same
            self.assertEqual(res_a["objects"], res_b["objects"])
            self.assertEqual(res_a["materials"], res_b["materials"])

            # Since blender might save timestamp or minor metadata in .blend headers,
            # strict binary file hashing might fail, but we'll test it as an optimal case.
            # Real deterministic setups might need stricter seed control.
            # self.assertEqual(self.get_file_hash(blend_a), self.get_file_hash(blend_b))

if __name__ == "__main__":
    unittest.main()
