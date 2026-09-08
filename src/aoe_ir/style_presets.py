from .appearance import (
    AppearanceProfile, AppearanceFamily, StyleProfile, StyleProfileType,
    ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, TextureProfile,
    RimLightProfile, SpecularProfile
)

class StylePresets:
    """Factory for predefined style configurations."""

    @staticmethod
    def create_anime(appearance_id: str = "anime_base") -> AppearanceProfile:
        return AppearanceProfile(
            appearance_id=appearance_id,
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                style_type=StyleProfileType.ANIME,
                shading=ShadingProfile(
                    model=ShaderModel.TOON,
                    band_count=2,
                    shadow_threshold=0.55,
                    shadow_softness=0.0,
                    rim_light=RimLightProfile(enabled=True, intensity=0.4, width=0.2),
                    specular=SpecularProfile(enabled=True, intensity=0.8, roughness=0.0)
                ),
                outline=OutlineProfile(
                    enabled=True,
                    method=OutlineMethod.INVERTED_HULL,
                    width=0.012,
                    color="#111111"
                ),
                texture=TextureProfile(mode="PAINTED")
            ),
            region_overrides={
                "FACE": StyleProfile(
                    style_type=StyleProfileType.ANIME,
                    shading=ShadingProfile(
                        model=ShaderModel.TOON,
                        band_count=1, # Often faces in anime have hard 1-band shadows
                        shadow_threshold=0.6,
                        rim_light=RimLightProfile(enabled=False) # Usually no rim light on face
                    )
                ),
                "HAIR": StyleProfile(
                    style_type=StyleProfileType.ANIME,
                    shading=ShadingProfile(
                        model=ShaderModel.TOON,
                        band_count=3,
                        specular=SpecularProfile(enabled=True, intensity=1.0, roughness=0.1) # Highlight rings
                    )
                )
            }
        )

    @staticmethod
    def create_comic(appearance_id: str = "comic_base") -> AppearanceProfile:
        return AppearanceProfile(
            appearance_id=appearance_id,
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                style_type=StyleProfileType.COMIC,
                shading=ShadingProfile(
                    model=ShaderModel.TOON,
                    band_count=4,
                    shadow_threshold=0.5,
                    shadow_color="#1a1a24",
                    rim_light=RimLightProfile(enabled=True, intensity=1.0, width=0.15)
                ),
                outline=OutlineProfile(
                    enabled=True,
                    method=OutlineMethod.INVERTED_HULL,
                    width=0.035, # Thicker for comic books
                    color="#000000"
                ),
                texture=TextureProfile(
                    mode="PAINTED",
                    use_curvature=True,
                    use_grunge=True,
                    use_hatching=True
                )
            )
        )

    @staticmethod
    def create_cartoon(appearance_id: str = "cartoon_base") -> AppearanceProfile:
        return AppearanceProfile(
            appearance_id=appearance_id,
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                style_type=StyleProfileType.CARTOON,
                shading=ShadingProfile(
                    model=ShaderModel.TOON,
                    band_count=3,
                    shadow_softness=0.15, # Softer transitions typical in western 3D cartoons
                    shadow_threshold=0.5,
                    rim_light=RimLightProfile(enabled=True, intensity=0.6, softness=0.3)
                ),
                outline=OutlineProfile(
                    enabled=True,
                    method=OutlineMethod.INVERTED_HULL,
                    width=0.02,
                    color="#333333"
                ),
                texture=TextureProfile(mode="PAINTED")
            )
        )
