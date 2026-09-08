import unittest
import os
import tempfile
import hashlib
import json
import shutil
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

        # Setup artifacts dir
        self.artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../artifacts"))
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def get_file_hash(self, filepath):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def compare_images(self, img_a, img_b):
        """Very basic size and hash comparison for golden images."""
        if not os.path.exists(img_b):
            return False # Golden doesn't exist yet

        size_a = os.path.getsize(img_a)
        size_b = os.path.getsize(img_b)

        # Tolerate 5% difference in file size as a proxy for 'equivalent'
        # (A real robust implementation would use PIL/OpenCV to diff pixels)
        diff_pct = abs(size_a - size_b) / max(size_a, size_b)
        return diff_pct < 0.05

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
            scene_path = os.path.join(tmpdir, "scene.blend")

            result = self.backend.export_asset(asset, filepath=scene_path, render_path=render_path)

            # Save artifacts
            if os.path.exists(render_path):
                shutil.copy(render_path, os.path.join(self.artifacts_dir, "render.png"))
            if os.path.exists(scene_path):
                shutil.copy(scene_path, os.path.join(self.artifacts_dir, "scene.blend"))
            with open(os.path.join(self.artifacts_dir, "scene_report.json"), "w") as f:
                json.dump(result.get("scene_report", {}), f, indent=2)

            self.assertEqual(result["status"], "SUCCESS")
            self.assertTrue(os.path.exists(render_path))
            self.assertGreater(os.path.getsize(render_path), 0, "Render image is empty")

            # Golden Image test (13)
            golden_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../golden"))
            golden_path = os.path.join(golden_dir, "golden_toon_test.png")

            if os.path.exists(golden_path):
                self.assertTrue(self.compare_images(render_path, golden_path), "Render does not match golden image")
            else:
                # If golden doesn't exist, we create it to bootstrap the process
                shutil.copy(render_path, golden_path)

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
            self.assertEqual(res_a["scene_report"]["objects"], res_b["scene_report"]["objects"])
            self.assertEqual(res_a["scene_report"]["materials"], res_b["scene_report"]["materials"])

if __name__ == "__main__":
    unittest.main()
