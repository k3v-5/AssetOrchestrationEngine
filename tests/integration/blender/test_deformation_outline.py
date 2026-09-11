import unittest
import os
import tempfile
import hashlib
import shutil
from src.aoe_ir.asset import AssetIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, OutlineProfile, OutlineMethod, ShadingProfile, ShaderModel
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner

class TestDeformationOutline(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

    def get_file_hash(self, filepath):
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def test_outline_deforms_with_armature(self):
        # We test that animating a rigged character with an outline produces
        # different renders for different poses, and the outline moves correctly with the base mesh
        asset = AssetIR(
            asset_id="MonkeyRigTest",
            appearance=AppearanceProfile(
                appearance_id="toon_rig",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON),
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.04)
                )
            )
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            hashes = []
            # We trigger the test_rig_pose parameter to simulate poses in the executor
            for i, pose_angle in enumerate([0.0, 0.5, -0.5]):
                render_path = os.path.join(tmpdir, f"render_pose_{i}.png")

                asset.metadata["test_rig_pose"] = pose_angle

                res = self.backend.export_asset(asset, render_path=render_path)

                self.assertTrue(os.path.exists(render_path))

                # Check explicitly the modifier order in the report if outline is enabled
                report = res.get("scene_report", {})
                if "MonkeyRigTest_Outline" in report.get("modifiers", {}):
                    mods = report["modifiers"]["MonkeyRigTest_Outline"]
                    # Assert that Armature is evaluated BEFORE the Solidify outline modifier
                    arm_idx = mods.index("Armature") if "Armature" in mods else -1
                    sol_idx = mods.index("Outline_Solidify") if "Outline_Solidify" in mods else -1
                    if arm_idx != -1 and sol_idx != -1:
                        self.assertLess(arm_idx, sol_idx, "Armature must evaluate before Solidify for correct outline deformation")

                hashes.append(self.get_file_hash(render_path))

            # Export the last deformed render to artifacts
            artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../artifacts"))
            os.makedirs(artifacts_dir, exist_ok=True)
            shutil.copy(render_path, os.path.join(artifacts_dir, "toon_deformed.png"))


            # The renders must be different if the mesh (and its outline) deformed
            self.assertNotEqual(hashes[0], hashes[1])
            self.assertNotEqual(hashes[1], hashes[2])
            self.assertNotEqual(hashes[0], hashes[2])

if __name__ == "__main__":
    unittest.main()
