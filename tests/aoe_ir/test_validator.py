import unittest
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, OutlineProfile
from src.aoe_ir.validation.appearance_validator import AppearanceValidator

class TestAppearanceValidator(unittest.TestCase):
    def test_pbr_validation_success(self):
        profile = AppearanceProfile(
            appearance_id="pbr_ok",
            family=AppearanceFamily.PBR,
            style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR))
        )
        result = AppearanceValidator.validate(profile)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.issues), 0)

    def test_pbr_validation_failure(self):
        profile = AppearanceProfile(
            appearance_id="pbr_fail",
            family=AppearanceFamily.PBR,
            style=StyleProfile(
                shading=ShadingProfile(model=ShaderModel.TOON),
                outline=OutlineProfile(enabled=True)
            )
        )
        result = AppearanceValidator.validate(profile)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.issues), 2)

    def test_npr_validation_success(self):
        profile = AppearanceProfile(
            appearance_id="npr_ok",
            family=AppearanceFamily.NPR,
            style=StyleProfile(shading=ShadingProfile(model=ShaderModel.TOON, band_count=3))
        )
        result = AppearanceValidator.validate(profile)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.issues), 0)

    def test_npr_validation_failure(self):
        profile = AppearanceProfile(
            appearance_id="npr_fail",
            family=AppearanceFamily.NPR,
            style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR))
        )
        result = AppearanceValidator.validate(profile)
        self.assertFalse(result.is_valid)
        self.assertEqual(len(result.issues), 1)

if __name__ == "__main__":
    unittest.main()
