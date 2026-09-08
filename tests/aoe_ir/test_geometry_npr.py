import unittest
from src.aoe_ir.asset import AssetIR, SemanticRegionIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, OutlineProfile, OutlineMethod, StyleProfileType
from src.aoe_ir.geometry.npr_processor import NPRGeometryProcessor

class TestNPRGeometryProcessor(unittest.TestCase):
    def test_inverted_hull(self):
        asset = AssetIR(
            asset_id="toon_char",
            semantic_regions={"face": SemanticRegionIR("face"), "body": SemanticRegionIR("body")},
            appearance=AppearanceProfile(
                appearance_id="anime_1",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL, width=0.02)
                ),
                region_overrides={
                    "face": StyleProfile(style_type=StyleProfileType.ANIME)
                }
            )
        )

        result = NPRGeometryProcessor.process(asset)

        self.assertTrue(result["outline_mesh_added"])
        self.assertEqual(result["outline_method"], "INVERTED_HULL")
        self.assertIn("face", result["processed_regions"])
        self.assertNotIn("body", result["processed_regions"]) # no override for body
        self.assertTrue(any("0.02" in msg for msg in result["messages"]))

    def test_no_outline(self):
        asset = AssetIR(
            asset_id="pbr_char",
            appearance=AppearanceProfile(
                appearance_id="pbr_1",
                family=AppearanceFamily.PBR,
                style=StyleProfile(outline=OutlineProfile(enabled=False))
            )
        )

        result = NPRGeometryProcessor.process(asset)

        self.assertFalse(result["outline_mesh_added"])
        self.assertEqual(result["outline_method"], "NONE")

if __name__ == "__main__":
    unittest.main()
