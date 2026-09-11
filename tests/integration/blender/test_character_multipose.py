import unittest
import os
import tempfile
import shutil
from src.aoe_ir.character import CharacterIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, StyleProfileType
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner
from tests.fixtures.humanoid_fixture import create_humanoid_fixture

class TestCharacterMultipose(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

        self.artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../artifacts"))
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def test_multipose_multiappearance(self):
        """
        Tests the identical character (same rig, same skinning, same semantic regions)
        under different poses (REST, POSE_A, POSE_B) and different appearances (PBR, Anime, Comic).
        """

        # 1. Define the appearance profiles
        pbr_app = AppearanceProfile(
            appearance_id="pbr_base",
            family=AppearanceFamily.PBR,
            style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR))
        )

        anime_app = AppearanceProfile(
            appearance_id="anime_toon",
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                shading=ShadingProfile(model=ShaderModel.TOON, band_count=2, shadow_threshold=0.55),
                outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.015)
            ),
            region_overrides={
                "FACE": StyleProfile(style_type=StyleProfileType.ANIME, shading=ShadingProfile(model=ShaderModel.TOON, band_count=1, shadow_threshold=0.7)),
                "HAIR": StyleProfile(style_type=StyleProfileType.ANIME, shading=ShadingProfile(model=ShaderModel.TOON, band_count=3, shadow_threshold=0.5))
            }
        )

        comic_app = AppearanceProfile(
            appearance_id="comic_toon",
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                shading=ShadingProfile(model=ShaderModel.TOON, band_count=4, shadow_threshold=0.45),
                outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.035)
            )
        )

        appearances = {
            "PBR": pbr_app,
            "ANIME": anime_app,
            "COMIC": comic_app
        }

        poses = ["REST", "pose_a", "pose_b"]

        with tempfile.TemporaryDirectory() as tmpdir:
            for app_name, app_profile in appearances.items():
                for pose_id in poses:
                    # Same character, just injecting the desired appearance and pose instruction
                    char_ir = create_humanoid_fixture(app_profile)
                    char_ir.character_id = f"Hero_{app_name}_{pose_id}"
                    char_ir.metadata["active_pose"] = pose_id

                    render_name = f"character_{app_name.lower()}_{pose_id.lower()}.png"
                    blend_name = f"character_{app_name.lower()}_{pose_id.lower()}.blend"

                    render_path = os.path.join(tmpdir, render_name)
                    blend_path = os.path.join(tmpdir, blend_name)

                    res = self.backend.export_asset(char_ir, filepath=blend_path, render_path=render_path)

                    self.assertEqual(res["status"], "SUCCESS", msg=res.get("error", res.get("traceback", "")))
                    self.assertTrue(os.path.exists(render_path))

                    # Copy to artifacts
                    shutil.copy(render_path, os.path.join(self.artifacts_dir, render_name))
                    if app_name == "ANIME" and pose_id == "pose_a":
                        # Save one blend file for inspection
                        shutil.copy(blend_path, os.path.join(self.artifacts_dir, "character_inspection.blend"))

                        # Validate deeper structure from report
                        report = res.get("scene_report", {})
                        self.assertIn("Hero_ANIME_pose_a_Armature", report.get("objects", []))
                        # Face override material should exist
                        self.assertTrue(any("FACE_Override" in mat for mat in report.get("materials", [])))

if __name__ == "__main__":
    unittest.main()
