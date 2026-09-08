import unittest
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, OutlineProfile, OutlineMethod, StyleProfileType, ShadingProfile, ShaderModel
from src.aoe_ir.asset import AssetIR
from src.aoe_ir.backends.blender import BlenderBackend
from src.aoe_ir.backends.base import BackendCapabilityError
from src.aoe_ir.backends.unreal import UnrealBackend

class TestBackendCapabilities(unittest.TestCase):
    def setUp(self):
        self.blender = BlenderBackend(use_real_executor=False)
        self.unreal = UnrealBackend()

    def test_blender_accepts_inverted_hull(self):
        asset = AssetIR(
            asset_id="Test1",
            appearance=AppearanceProfile(
                appearance_id="toon_1",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON),
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL)
                )
            )
        )
        # Should not raise exception
        res = self.blender.export_asset(asset)
        self.assertEqual(res["status"], "SUCCESS (SIMULATED)")

    def test_blender_rejects_post_process(self):
        asset = AssetIR(
            asset_id="Test2",
            appearance=AppearanceProfile(
                appearance_id="toon_2",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON),
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.POST_PROCESS)
                )
            )
        )
        with self.assertRaises(BackendCapabilityError):
            self.blender.export_asset(asset)

    def test_unreal_rejects_inverted_hull(self):
        asset = AssetIR(
            asset_id="Test3",
            appearance=AppearanceProfile(
                appearance_id="toon_3",
                family=AppearanceFamily.NPR,
                style=StyleProfile(
                    shading=ShadingProfile(model=ShaderModel.TOON),
                    outline=OutlineProfile(enabled=True, method=OutlineMethod.INVERTED_HULL)
                )
            )
        )
        with self.assertRaises(BackendCapabilityError):
            self.unreal.export_asset(asset)

if __name__ == "__main__":
    unittest.main()
