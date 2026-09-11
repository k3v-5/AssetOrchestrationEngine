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

    def compare_images(self, img_a, img_b, threshold=5.0):
        """Perceptual image comparison using Root Mean Square Error via Pillow."""
        import math
        try:
            from PIL import Image, ImageChops
        except ImportError:
            # Fallback if pillow not installed
            size_a = os.path.getsize(img_a)
            size_b = os.path.getsize(img_b)
            return abs(size_a - size_b) / max(size_a, size_b) < 0.05

        if not os.path.exists(img_b):
            return False # Golden doesn't exist yet

        im1 = Image.open(img_a).convert("RGB")
        im2 = Image.open(img_b).convert("RGB")

        if im1.size != im2.size:
            return False

        diff = ImageChops.difference(im1, im2)
        h = diff.histogram()
        sq = (value * ((idx % 256)**2) for idx, value in enumerate(h))
        rms = math.sqrt(sum(sq) / float(im1.size[0] * im1.size[1]))

        # RMS represents an absolute average color difference per pixel (0 to 255).
        return rms <= threshold

    def test_real_render_output(self):
        # 12. RENDER REAL - Generate actual .png renders for PBR and NPR

        test_cases = [
            ("pbr_test.png", AppearanceProfile(appearance_id="pbr_1", family=AppearanceFamily.PBR, style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR)))),
            ("toon_2band.png", AppearanceProfile(appearance_id="toon_2", family=AppearanceFamily.NPR, style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=2)))),
            ("toon_3band.png", AppearanceProfile(appearance_id="toon_3", family=AppearanceFamily.NPR, style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=3)))),
            ("toon_4band.png", AppearanceProfile(appearance_id="toon_4", family=AppearanceFamily.NPR, style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=4)))),
            ("toon_outline.png", AppearanceProfile(appearance_id="toon_out", family=AppearanceFamily.NPR, style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=2), outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.03))))
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            for render_name, appearance in test_cases:
                asset = AssetIR(asset_id=f"Test_{render_name.split('.')[0]}", appearance=appearance)
                render_path = os.path.join(tmpdir, render_name)

                result = self.backend.export_asset(asset, render_path=render_path)

                # Save artifacts
                if os.path.exists(render_path):
                    shutil.copy(render_path, os.path.join(self.artifacts_dir, render_name))

                self.assertEqual(result["status"], "SUCCESS")
                self.assertTrue(os.path.exists(render_path))
                self.assertGreater(os.path.getsize(render_path), 0, f"Render image {render_name} is empty")

            # Keep one scene report and blend for artifact reference
            with open(os.path.join(self.artifacts_dir, "scene_report.json"), "w") as f:
                json.dump(result.get("scene_report", {}), f, indent=2)

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
