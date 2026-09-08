import unittest
import os
import tempfile
import json
from src.aoe_ir.asset import AssetIR, SemanticRegionIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, OutlineProfile, OutlineMethod, StyleProfileType, ShadingProfile, ShaderModel
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner

class TestAssetGenerationIntegration(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

    def test_toon_basic_material_real(self):
        # TERCER TEST: MATERIAL TOON REAL
        asset = AssetIR(
            asset_id="MonkeyToon",
            appearance=AppearanceProfile(
                appearance_id="toon_1",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON, band_count=2, shadow_threshold=0.45)
                )
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            blend_path = os.path.join(tmpdir, "toon.blend")
            result = self.backend.export_asset(asset, filepath=blend_path)

            self.assertEqual(result["status"], "SUCCESS", result.get("error", ""))
            self.assertTrue(os.path.exists(blend_path))

            # Verify via deep scene report
            report = result.get("scene_report", {})
            self.assertIn("MonkeyToon", report.get("objects", []))
            self.assertTrue(any("MonkeyToon_Toon" in mat for mat in report.get("materials", [])), "Toon material not created in Blender")

    def test_inverted_hull_real(self):
        # CUARTO TEST: INVERTED HULL REAL
        asset = AssetIR(
            asset_id="MonkeyOutline",
            appearance=AppearanceProfile(
                appearance_id="toon_outline",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON),
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.02)
                )
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            blend_path = os.path.join(tmpdir, "outline.blend")
            result = self.backend.export_asset(asset, filepath=blend_path)

            self.assertEqual(result["status"], "SUCCESS")

            report = result.get("scene_report", {})
            # The outline object should exist physically in Blender
            self.assertIn("MonkeyOutline_Outline", report.get("objects", []))
            # The modifier should be present
            self.assertIn("Outline_Solidify", report.get("modifiers", {}).get("MonkeyOutline_Outline", []))
            # Outline material exists
            self.assertIn("Mat_Outline", report.get("materials", []))

    def test_semantic_regions_real(self):
        # QUINTO TEST: SEMANTIC REGIONS
        asset = AssetIR(
            asset_id="MonkeySemantic",
            semantic_regions={"FACE": SemanticRegionIR("FACE", vertex_indices=[0, 1, 2])},
            appearance=AppearanceProfile(
                appearance_id="toon_semantic",
                family=AppearanceFamily.NPR,
                style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON)),
                region_overrides={
                    "FACE": StyleProfile(style_type="ANIME")
                }
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.backend.export_asset(asset, filepath=os.path.join(tmpdir, "semantic.blend"))
            self.assertEqual(result["status"], "SUCCESS")

            report = result.get("scene_report", {})
            # Should have the base toon material AND the FACE override material
            self.assertTrue(any("Mat_MonkeySemantic_Toon" in mat for mat in report.get("materials", [])))
            self.assertTrue(any("Mat_MonkeySemantic_FACE_Override" in mat for mat in report.get("materials", [])))

    def test_pbr_regression_real(self):
        # SEXTO TEST: PBR REGRESSION
        asset = AssetIR(
            asset_id="MonkeyPBR",
            appearance=AppearanceProfile(
                appearance_id="pbr_base",
                family=AppearanceFamily.PBR,
                style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR))
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            blend_path = os.path.join(tmpdir, "pbr.blend")
            result = self.backend.export_asset(asset, filepath=blend_path)

            self.assertEqual(result["status"], "SUCCESS")
            self.assertTrue(os.path.exists(blend_path))

            report = result.get("scene_report", {})
            self.assertTrue(any("Mat_MonkeyPBR_PBR" in mat for mat in report.get("materials", [])))

if __name__ == "__main__":
    unittest.main()
