import unittest
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod
from src.aoe_ir.asset import AssetIR
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.unreal import UnrealBackend

class TestBackends(unittest.TestCase):
    def setUp(self):
        self.pbr_asset = AssetIR(
            asset_id="test_pbr",
            appearance=AppearanceProfile(
                appearance_id="pbr_1",
                family=AppearanceFamily.PBR,
                style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR))
            )
        )

        self.npr_asset = AssetIR(
            asset_id="test_npr",
            appearance=AppearanceProfile(
                appearance_id="npr_1",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON, band_count=4),
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL)
                )
            )
        )

    def test_blender_backend(self):
        backend = BlenderBackend()

        # Test PBR
        pbr_res = backend.export_asset(self.pbr_asset)
        self.assertIn("PBR_OUTPUT", pbr_res["generated_nodes"])

        # Test NPR
        npr_res = backend.export_asset(self.npr_asset)
        self.assertIn("TOON_RAMP", npr_res["generated_nodes"])
        self.assertEqual(npr_res["generated_nodes"]["TOON_BANDS"], 4)
        self.assertEqual(npr_res["generated_nodes"]["OUTLINE"], "INVERTED_HULL")

    def test_unreal_backend(self):
        backend = UnrealBackend()

        # Test PBR
        pbr_res = backend.export_asset(self.pbr_asset)
        self.assertEqual(pbr_res["master_material"], "/Engine/MasterMaterials/M_PBR_Master")

        # Test NPR
        npr_res = backend.export_asset(self.npr_asset)
        self.assertEqual(npr_res["master_material"], "/Engine/MasterMaterials/M_NPR_Anime_Master")

if __name__ == "__main__":
    unittest.main()
