import unittest
from src.aoe_ir.appearance import (
    AppearanceProfile, AppearanceFamily, StyleProfile, StyleProfileType,
    ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, TextureProfile
)

class TestAppearanceIR(unittest.TestCase):
    def test_pbr_profile(self):
        profile = AppearanceProfile(
            appearance_id="pbr_default",
            family=AppearanceFamily.PBR,
            style=StyleProfile(
                style_type=StyleProfileType.REALISTIC,
                shading=ShadingProfile(model=ShaderModel.PBR)
            )
        )
        self.assertEqual(profile.family, AppearanceFamily.PBR)
        self.assertEqual(profile.style.style_type, StyleProfileType.REALISTIC)

    def test_anime_profile(self):
        profile = AppearanceProfile(
            appearance_id="anime_hero",
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                style_type=StyleProfileType.ANIME,
                shading=ShadingProfile(
                    model=ShaderModel.TOON,
                    band_count=3,
                    shadow_threshold=0.55,
                    shadow_color="#526080"
                ),
                outline=OutlineProfile(
                    enabled=True,
                    method=OutlineMethod.INVERTED_HULL,
                    width=0.012
                )
            ),
            region_overrides={
                "face": StyleProfile(
                    style_type=StyleProfileType.ANIME,
                    shading=ShadingProfile(
                        model=ShaderModel.TOON,
                        shadow_threshold=0.7 # Face has different shadow threshold
                    )
                )
            }
        )
        self.assertEqual(profile.family, AppearanceFamily.NPR)
        self.assertEqual(profile.style.style_type, StyleProfileType.ANIME)
        self.assertTrue(profile.style.outline.enabled)
        self.assertEqual(profile.style.outline.method, OutlineMethod.INVERTED_HULL)
        self.assertIn("face", profile.region_overrides)

if __name__ == "__main__":
    unittest.main()
