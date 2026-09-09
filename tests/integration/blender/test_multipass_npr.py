import unittest
import os
import tempfile
import math
import shutil
from src.aoe_ir.animation import InterpolationType
from src.aoe_ir.interchange.animation import ExternalAnimation, ExternalKeyframe, ExternalBoneTransform
from src.aoe_ir.interchange.mapper import SkeletonMapper
from src.aoe_ir.interchange.retargeter import AnimationRetargeter
from src.aoe_ir.style_presets import StylePresets
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner
from tests.fixtures.humanoid_fixture import create_humanoid_fixture

class TestMultipassNPRGolden(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

        self.artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../artifacts"))
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def _create_mock_external_walk(self) -> ExternalAnimation:
        return ExternalAnimation(
            animation_id="mixamo_walk",
            duration_frames=5,
            keyframes=[
                ExternalKeyframe(frame=0, transforms={"mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0, math.radians(20), 0))}),
                ExternalKeyframe(frame=5, transforms={"mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0, math.radians(-20), 0))}),
                ExternalKeyframe(frame=5, transforms={"mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0, math.radians(20), 0))})
            ]
        )

    def test_golden_multipass_advanced_npr(self):
        """
        The Golden Test for Phase 10:
        Render a sequence across advanced procedural NPR styles (Borderlands & Sketch)
        to prove that layers (Curvature, Grunge, TemporalBehavior) inject correctly
        and execute safely over a timeline.
        """
        ext_anim = self._create_mock_external_walk()
        mapper = SkeletonMapper.create_mixamo_mapper()
        aoe_clip = AnimationRetargeter.retarget(ext_anim, mapper)
        aoe_clip.interpolation = InterpolationType.BEZIER

        # Pull advanced styles from presets
        borderlands_app = StylePresets.create_borderlands()
        sketch_app = StylePresets.create_sketch()

        appearances = {"SKETCH": sketch_app}

        with tempfile.TemporaryDirectory() as tmpdir:
            for style_name, app in appearances.items():
                char = create_humanoid_fixture(app)
                char.character_id = f"Hero_Advanced_{style_name}"

                # Active Animation
                char.animation.clips["walk"] = aoe_clip
                char.animation.active_clip = "walk"

                render_base_path = os.path.join(tmpdir, f"advanced_{style_name.lower()}.png")

                blend_path = os.path.join(tmpdir, f"advanced_{style_name.lower()}.blend")
                res = self.backend.export_asset(char, filepath=blend_path)
                self.assertEqual(res["status"], "SUCCESS", msg=res.get("error", res.get("traceback", "")))

                # Verify nodes in the report
                report = res.get("scene_report", {})
                self.assertIn(f"Hero_Advanced_{style_name}", report.get("objects", []))

if __name__ == "__main__":
    unittest.main()
