import unittest
import os
import tempfile
import shutil
from src.aoe_ir.character import CharacterIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, StyleProfileType
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.style_presets import StylePresets
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner
from tests.fixtures.humanoid_fixture import create_humanoid_fixture

class TestTemporalNPRStability(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

        self.artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../artifacts"))
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def test_temporal_stability_comic(self):
        # We test that a continuous animation generates stable renders
        # without randomly breaking outline or mesh assignments over time.
        app = StylePresets.create_comic()

        char_ir = create_humanoid_fixture(app)
        char_ir.character_id = "Temporal_Hero_Comic"

        # Select an active clip instead of static pose
        char_ir.animation.active_clip = "pose_c"
        char_ir.animation.clips["pose_c"].duration_frames = 5 # Short 5-frame animation to save CI time

        with tempfile.TemporaryDirectory() as tmpdir:
            render_base_path = os.path.join(tmpdir, "temporal_seq.png")
            res = self.backend.export_asset(char_ir, render_path=render_base_path)

            self.assertEqual(res["status"], "SUCCESS")

            # Since we requested a 5 frame sequence, Blender outputs frame 0 to 5 (6 frames)
            # They should be named temporal_seq_0000.png, temporal_seq_0001.png...

            frames_found = 0
            for i in range(6):
                frame_file = f"temporal_seq_{str(i).zfill(4)}.png"
                frame_path = os.path.join(tmpdir, frame_file)
                if os.path.exists(frame_path):
                    frames_found += 1
                    shutil.copy(frame_path, os.path.join(self.artifacts_dir, frame_file))

            # Ensure Blender generated a sequence
            self.assertGreaterEqual(frames_found, 2, "Failed to render sequence of frames")

            # Check structure stability
            report = res.get("scene_report", {})
            self.assertIn("Temporal_Hero_Comic_Outline", report.get("objects", []))

            mods = report.get("modifiers", {}).get("Temporal_Hero_Comic_Outline", [])
            self.assertIn("Armature", mods)
            self.assertIn("Outline_Solidify", mods)
            # Solidify must be AFTER Armature for temporal stability
            self.assertLess(mods.index("Armature"), mods.index("Outline_Solidify"))

if __name__ == "__main__":
    unittest.main()
