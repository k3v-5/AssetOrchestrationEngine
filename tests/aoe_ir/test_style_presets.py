import unittest
from src.aoe_ir.style_presets import StylePresets
from src.aoe_ir.appearance import StyleProfileType

class TestStylePresets(unittest.TestCase):
    def test_anime_preset(self):
        app = StylePresets.create_anime()
        self.assertEqual(app.style.style_type, StyleProfileType.ANIME)
        self.assertTrue(app.style.shading.rim_light.enabled)
        # Verify region overrides
        self.assertIn("FACE", app.region_overrides)
        self.assertFalse(app.region_overrides["FACE"].shading.rim_light.enabled)
        self.assertEqual(app.region_overrides["FACE"].shading.band_count, 1)

    def test_comic_preset(self):
        app = StylePresets.create_comic()
        self.assertEqual(app.style.style_type, StyleProfileType.COMIC)
        self.assertEqual(app.style.shading.band_count, 4)
        self.assertTrue(app.style.texture.use_hatching)
        self.assertTrue(app.style.texture.use_curvature)

    def test_cartoon_preset(self):
        app = StylePresets.create_cartoon()
        self.assertEqual(app.style.style_type, StyleProfileType.CARTOON)
        self.assertEqual(app.style.shading.band_count, 3)
        self.assertEqual(app.style.shading.shadow_softness, 0.15)

if __name__ == "__main__":
    unittest.main()
