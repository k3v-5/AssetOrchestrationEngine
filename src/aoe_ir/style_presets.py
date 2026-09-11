from .appearance import (
    AppearanceProfile, AppearanceFamily, StyleProfile, StyleProfileType,
    ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, TextureProfile,
    RimLightProfile, SpecularProfile, NPRProfileIR, StyleLayerIR, CurvatureLayerIR, GrungeLayerIR, HatchingLayerIR, TemporalBehaviorIR
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
                npr_profile=NPRProfileIR(
                    layers=StyleLayerIR(
                        curvature=CurvatureLayerIR(enabled=True, intensity=1.2, cavity_color="#111122"),
                        grunge=GrungeLayerIR(enabled=True, intensity=0.6, scale=15.0)
                    )
                )
            )
        )

    @staticmethod
    def create_borderlands(appearance_id: str = "borderlands_base") -> AppearanceProfile:
        return AppearanceProfile(
            appearance_id=appearance_id,
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                style_type=StyleProfileType.STYLIZED,
                shading=ShadingProfile(
                    model=ShaderModel.TOON,
                    band_count=3,
                    shadow_threshold=0.45,
                    shadow_color="#2b2b2b",
                    rim_light=RimLightProfile(enabled=True, intensity=0.8, width=0.2)
                ),
                outline=OutlineProfile(
                    enabled=True,
                    method=OutlineMethod.INVERTED_HULL,
                    width=0.025,
                    color="#000000"
                ),
                npr_profile=NPRProfileIR(
                    layers=StyleLayerIR(
                        curvature=CurvatureLayerIR(enabled=True, intensity=2.0, cavity_color="#000000"),
                        grunge=GrungeLayerIR(enabled=True, intensity=1.5, scale=20.0, color="#1a1a1a"),
                        hatching=HatchingLayerIR(enabled=True, intensity=0.7, scale=8.0)
                    )
                )
            )
        )

    @staticmethod
    def create_sketch(appearance_id: str = "sketch_base") -> AppearanceProfile:
        return AppearanceProfile(
            appearance_id=appearance_id,
            family=AppearanceFamily.NPR,
            style=StyleProfile(
                style_type=StyleProfileType.SKETCH,
                shading=ShadingProfile(
                    model=ShaderModel.TOON,
                    band_count=2,
                    shadow_color="#444444",
                    highlight_color="#f0f0f0"
                ),
                outline=OutlineProfile(
                    enabled=True,
                    method=OutlineMethod.INVERTED_HULL,
                    width=0.01
                ),
                npr_profile=NPRProfileIR(
                    layers=StyleLayerIR(
                        hatching=HatchingLayerIR(enabled=True, coordinate_space="SCREEN", rotation_angle=45.0),
                        temporal=TemporalBehaviorIR(enabled=True, update_rate=3) # Update sketch lines every 3 frames
                    )
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
