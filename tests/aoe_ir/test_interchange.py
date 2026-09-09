import unittest
from src.aoe_ir.interchange.animation import ExternalAnimation, ExternalKeyframe, ExternalBoneTransform
from src.aoe_ir.interchange.mapper import SkeletonMapper, SkeletonMapConfig

class TestInterchange(unittest.TestCase):
    def test_mixamo_mapper(self):
        mapper = SkeletonMapper.create_mixamo_mapper()
        self.assertEqual(mapper.bone_map["mixamorig:RightArm"], "upper_arm_R")
        self.assertEqual(mapper.bone_map["mixamorig:Head"], "head")

    def test_external_animation_structure(self):
        anim = ExternalAnimation(
            animation_id="ext_walk",
            duration_frames=10,
            keyframes=[
                ExternalKeyframe(frame=0, transforms={"mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0,1,0))}),
                ExternalKeyframe(frame=5, transforms={"mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0,2,0))})
            ]
        )
        self.assertEqual(len(anim.keyframes), 2)
        self.assertEqual(anim.keyframes[1].transforms["mixamorig:RightArm"].rotation_euler[1], 2)

if __name__ == "__main__":
    unittest.main()

from src.aoe_ir.interchange.retargeter import AnimationRetargeter

class TestRetargeting(unittest.TestCase):
    def test_retarget_external_anim(self):
        anim = ExternalAnimation(
            animation_id="ext_walk",
            duration_frames=10,
            keyframes=[
                ExternalKeyframe(frame=0, transforms={"mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0,1,0))}),
                ExternalKeyframe(frame=5, transforms={"mixamorig:RightArm": ExternalBoneTransform(rotation_euler=(0,2,0))})
            ]
        )
        mapper = SkeletonMapper.create_mixamo_mapper()

        aoe_clip = AnimationRetargeter.retarget(anim, mapper)

        self.assertEqual(aoe_clip.clip_id, "ext_walk")
        self.assertEqual(aoe_clip.duration_frames, 10)
        self.assertIn("upper_arm_R", aoe_clip.keyframes[0].bone_transforms)
        self.assertEqual(aoe_clip.keyframes[5].bone_transforms["upper_arm_R"].rotation_euler[1], 2)
