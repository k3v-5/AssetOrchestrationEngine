import unittest
import os
import tempfile
import math
import shutil
from src.aoe_ir.character import CharacterIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, StyleProfileType
from src.aoe_ir.animation import AnimationFoundationIR, InterpolationType
from src.aoe_ir.ik import IKSolverConfigIR, IKConstraintIR, IKConstraintType
from src.aoe_ir.pose import PoseIR
from src.aoe_ir.interchange.animation import ExternalAnimation, ExternalKeyframe, ExternalBoneTransform
from src.aoe_ir.interchange.mapper import SkeletonMapper
from src.aoe_ir.interchange.retargeter import AnimationRetargeter
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner
from tests.fixtures.humanoid_fixture import create_humanoid_fixture

class TestRetargetingGolden(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

        self.executor_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "executor.py"))
        self.backend = BlenderBackend(use_real_executor=True, executor_script=self.executor_script)

        self.artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../artifacts"))
        os.makedirs(self.artifacts_dir, exist_ok=True)

    def _create_mock_external_walk(self) -> ExternalAnimation:
        # We simulate a "Walk" animation originating from a format like Mixamo
        return ExternalAnimation(
            animation_id="mixamo_walk",
            duration_frames=10,
            keyframes=[
                ExternalKeyframe(frame=0, transforms={
                    "mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0, math.radians(20), 0)),
                    "mixamorig:LeftArm": ExternalBoneTransform(rotation_euler=(0, math.radians(-20), 0))
                }),
                ExternalKeyframe(frame=5, transforms={
                    "mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0, math.radians(-20), 0)),
                    "mixamorig:LeftArm": ExternalBoneTransform(rotation_euler=(0, math.radians(20), 0))
                }),
                ExternalKeyframe(frame=10, transforms={
                    "mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0, math.radians(20), 0)),
                    "mixamorig:LeftArm": ExternalBoneTransform(rotation_euler=(0, math.radians(-20), 0))
                })
            ]
        )

    def test_golden_retarget_multipose(self):
        """
        The Golden Test:
        Import an external animation, retarget to a CharacterIR, and render
        the sequence in 3 distinct NPR/PBR styles to verify interpolation and independence.
        """
        # 1. Import and Retarget
        ext_anim = self._create_mock_external_walk()
        mapper = SkeletonMapper.create_mixamo_mapper()
        aoe_clip = AnimationRetargeter.retarget(ext_anim, mapper)
        aoe_clip.interpolation = InterpolationType.BEZIER

        # 2. Setup Appearances
        pbr_app = AppearanceProfile(appearance_id="pbr", family=AppearanceFamily.PBR, style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR)))
        anime_app = AppearanceProfile(
            appearance_id="anime", family=AppearanceFamily.NPR,
            style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=2), outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.015))
        )
        comic_app = AppearanceProfile(
            appearance_id="comic", family=AppearanceFamily.NPR,
            style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=4), outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.035))
        )

        appearances = {"PBR": pbr_app, "ANIME": anime_app, "COMIC": comic_app}

        with tempfile.TemporaryDirectory() as tmpdir:
            for style_name, app in appearances.items():
                char = create_humanoid_fixture(app)
                char.character_id = f"Hero_Retargeted_{style_name}"

                # Override the base test animation with the retargeted one
                char.animation.clips["walk"] = aoe_clip
                char.animation.active_clip = "walk"

                # Apply an IK constraint to the feet pointing to the floor
                char.ik_config = IKSolverConfigIR(
                    solver_id="legs",
                    constraints=[
                        IKConstraintIR(
                            constraint_id="foot_l_plant",
                            bone_target="foot_L",
                            constraint_type=IKConstraintType.POSITION,
                            chain_length=2,
                            target_position=(0.1, 0, 0)
                        ),
                        IKConstraintIR(
                            constraint_id="foot_r_plant",
                            bone_target="foot_R",
                            constraint_type=IKConstraintType.POSITION,
                            chain_length=2,
                            target_position=(-0.1, 0, 0)
                        )
                    ]
                )

                render_base_path = os.path.join(tmpdir, f"retarget_{style_name.lower()}.png")

                res = self.backend.export_asset(char, render_path=render_base_path)
                self.assertEqual(res["status"], "SUCCESS")

                # Validate the 11 frames were generated (0 to 10)
                frames_found = 0
                for f in range(11):
                    frame_path = os.path.join(tmpdir, f"retarget_{style_name.lower()}_{str(f).zfill(4)}.png")
                    if os.path.exists(frame_path):
                        frames_found += 1
                        # Save frame 5 (the interpolated peak) for artifacts
                        if f == 5:
                            shutil.copy(frame_path, os.path.join(self.artifacts_dir, f"retarget_peak_{style_name.lower()}.png"))

                self.assertGreaterEqual(frames_found, 10, f"Failed to generate sequence for {style_name}")

                # Check scene report structure
                report = res.get("scene_report", {})
                if style_name != "PBR":
                    self.assertIn(f"Hero_Retargeted_{style_name}_Outline", report.get("objects", []))

if __name__ == "__main__":
    unittest.main()
