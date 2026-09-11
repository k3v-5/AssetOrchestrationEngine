import unittest
from src.aoe_ir.animation import AnimationFoundationIR, AnimationClipIR
from src.aoe_ir.pose import PoseIR
from src.aoe_ir.validation.animation_validator import AnimationValidator

class TestAnimationIR(unittest.TestCase):
    def setUp(self):
        self.anim = AnimationFoundationIR(
            rest_pose=PoseIR(pose_id="REST"),
            clips={
                "walk": AnimationClipIR(
                    clip_id="walk",
                    duration_frames=30,
                    keyframes={
                        0: PoseIR("walk_0"),
                        15: PoseIR("walk_15"),
                        30: PoseIR("walk_30")
                    }
                )
            }
        )

    def test_validation_success(self):
        res = AnimationValidator.validate(self.anim)
        self.assertTrue(res.is_valid)

    def test_validation_fail_negative_frame(self):
        self.anim.clips["walk"].keyframes[-5] = PoseIR("bad")
        res = AnimationValidator.validate(self.anim)
        self.assertFalse(res.is_valid)

    def test_validation_fail_out_of_bounds(self):
        self.anim.clips["walk"].keyframes[35] = PoseIR("bad")
        res = AnimationValidator.validate(self.anim)
        self.assertFalse(res.is_valid)

if __name__ == "__main__":
    unittest.main()
