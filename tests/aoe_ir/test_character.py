import unittest
from src.aoe_ir.character import CharacterIR, CharacterMeshIR, SemanticRegionTag, CharacterSemanticRegionIR
from src.aoe_ir.skeleton import SkeletonIR, BoneIR, SkinningIR, VertexWeightIR
from src.aoe_ir.validation.character_validator import CharacterValidator

class TestCharacterIR(unittest.TestCase):
    def setUp(self):
        self.char = CharacterIR(
            character_id="hero_01",
            meshes={"body_mesh": CharacterMeshIR("body_mesh", vertex_count=100)},
            skeleton=SkeletonIR(
                skeleton_id="humanoid_base",
                root_bone="root",
                bones={
                    "root": BoneIR("root", children=["spine"]),
                    "spine": BoneIR("spine", parent="root")
                }
            ),
            skinning={
                "body_mesh": SkinningIR(
                    skinning_id="body_skin",
                    vertex_weights=[
                        VertexWeightIR(vertex_index=0, weights={"root": 0.5, "spine": 0.5}),
                        VertexWeightIR(vertex_index=1, weights={"spine": 1.0})
                    ]
                )
            },
            semantic_regions=[
                CharacterSemanticRegionIR(region_id=SemanticRegionTag.BODY, mesh_id="body_mesh", vertex_indices=[0, 1])
            ]
        )

    def test_character_validation_success(self):
        result = CharacterValidator.validate(self.char)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.issues), 0)

    def test_character_validation_fails_normalization(self):
        self.char.skinning["body_mesh"].vertex_weights.append(
            VertexWeightIR(vertex_index=2, weights={"spine": 0.7, "root": 0.5}) # Sum = 1.2
        )
        result = CharacterValidator.validate(self.char)
        self.assertFalse(result.is_valid)
        self.assertIn("sum to 1.0", result.issues[0])

    def test_character_validation_fails_unknown_bone(self):
        self.char.skinning["body_mesh"].vertex_weights.append(
            VertexWeightIR(vertex_index=3, weights={"arm_L": 1.0})
        )
        result = CharacterValidator.validate(self.char)
        self.assertFalse(result.is_valid)
        self.assertIn("unknown bone", result.issues[0])

if __name__ == "__main__":
    unittest.main()
