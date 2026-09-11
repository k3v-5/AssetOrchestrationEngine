import unittest
from src.aoe_ir.facial import FaceRigIR, BlendShapeIR, ExpressionProfileIR, ExpressionComponentIR, FacialChannelType

class TestFacialIR(unittest.TestCase):
    def test_expression_composition(self):
        facerig = FaceRigIR(
            rig_id="hero_face",
            blend_shapes={
                "mouth_smile": BlendShapeIR("shape_1", "body_mesh", "MouthSmile"),
                "eye_squint": BlendShapeIR("shape_2", "body_mesh", "EyeSquint")
            },
            expressions={
                "Happy": ExpressionProfileIR("Happy", components=[
                    ExpressionComponentIR("mouth_smile", FacialChannelType.BLENDSHAPE, 0.8),
                    ExpressionComponentIR("eye_squint", FacialChannelType.BLENDSHAPE, 0.4),
                    ExpressionComponentIR("cheek_raise", FacialChannelType.BONE, 0.2)
                ])
            }
        )

        self.assertEqual(len(facerig.expressions["Happy"].components), 3)
        self.assertEqual(facerig.expressions["Happy"].components[2].channel_type, FacialChannelType.BONE)

if __name__ == "__main__":
    unittest.main()

from src.aoe_ir.facial import PhonemeEventIR, LipSyncTrackIR, VisemeMappingIR

class TestLipSyncIR(unittest.TestCase):
    def test_lipsync_structure(self):
        track = LipSyncTrackIR(
            track_id="dialogue_01",
            phonemes=[
                PhonemeEventIR(time=0.0, phoneme="SIL"),
                PhonemeEventIR(time=0.12, phoneme="A"),
                PhonemeEventIR(time=0.24, phoneme="M")
            ]
        )

        viseme = VisemeMappingIR(
            viseme_id="Viseme_A",
            phoneme_triggers=["A"],
            expression_id="Mouth_Open_Wide"
        )

        self.assertEqual(len(track.phonemes), 3)
        self.assertEqual(viseme.phoneme_triggers[0], "A")
