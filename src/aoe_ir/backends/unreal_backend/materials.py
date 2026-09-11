from ...appearance import AppearanceProfile, AppearanceFamily
from .manifest import ManifestMaterialInstanceInfo

class UnrealMaterialTranslator:
    @staticmethod
    def resolve_master_material(app: AppearanceProfile) -> str:
        if app.family == AppearanceFamily.PBR:
            return "/Game/AOE/Materials/M_AOE_PBR_Master"
        elif app.family == AppearanceFamily.NPR:
            return "/Game/AOE/Materials/M_AOE_NPR_Master"
        return "/Game/AOE/Materials/M_AOE_Default"

    @staticmethod
    def hex_to_rgba(hex_str: str) -> list[float]:
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:
            r, g, b = tuple(int(hex_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))
            return [r, g, b, 1.0]
        return [1.0, 1.0, 1.0, 1.0]

    @staticmethod
    def generate_instance_parameters(app: AppearanceProfile, char_id: str) -> ManifestMaterialInstanceInfo:
        instance_info = ManifestMaterialInstanceInfo(
            name=f"MI_{char_id}",
            parent=UnrealMaterialTranslator.resolve_master_material(app)
        )

        if app.family == AppearanceFamily.NPR:
            shading = app.style.shading
            layers = app.style.npr_profile.layers if app.style.npr_profile else None

            instance_info.vector_parameters = {
                "ShadowColor": UnrealMaterialTranslator.hex_to_rgba(shading.shadow_color),
                "MidtoneColor": UnrealMaterialTranslator.hex_to_rgba(shading.midtone_color),
                "HighlightColor": UnrealMaterialTranslator.hex_to_rgba(shading.highlight_color),
            }

            instance_info.scalar_parameters = {
                "BandCount": float(shading.band_count),
                "ShadowThreshold": shading.shadow_threshold,
                "ShadowSoftness": shading.shadow_softness,
            }

            if shading.rim_light.enabled:
                instance_info.scalar_parameters["RimIntensity"] = shading.rim_light.intensity
                instance_info.vector_parameters["RimColor"] = UnrealMaterialTranslator.hex_to_rgba(shading.rim_light.color)

            if layers:
                if layers.curvature.enabled:
                    instance_info.scalar_parameters["CurvatureIntensity"] = layers.curvature.intensity
                if layers.grunge.enabled:
                    instance_info.scalar_parameters["GrungeIntensity"] = layers.grunge.intensity

        return instance_info
