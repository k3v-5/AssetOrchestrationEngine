from ...appearance import AppearanceProfile, AppearanceFamily

class UnrealMaterialTranslator:
    @staticmethod
    def resolve_master_material(app: AppearanceProfile) -> str:
        if app.family == AppearanceFamily.PBR:
            return "/Game/AOE/Materials/M_AOE_PBR_Master"
        elif app.family == AppearanceFamily.NPR:
            return "/Game/AOE/Materials/M_AOE_NPR_Master"
        return "/Game/AOE/Materials/M_AOE_Default"

    @staticmethod
    def generate_instance_parameters(app: AppearanceProfile) -> dict:
        params = {}
        if app.family == AppearanceFamily.NPR:
            shading = app.style.shading
            layers = app.style.npr_profile.layers if app.style.npr_profile else None

            params["VectorParameterValues"] = {
                "ShadowColor": shading.shadow_color,
                "MidtoneColor": shading.midtone_color,
                "HighlightColor": shading.highlight_color,
            }
            params["ScalarParameterValues"] = {
                "BandCount": shading.band_count,
                "ShadowThreshold": shading.shadow_threshold,
                "ShadowSoftness": shading.shadow_softness,
            }
            if shading.rim_light.enabled:
                params["ScalarParameterValues"]["RimIntensity"] = shading.rim_light.intensity
                params["VectorParameterValues"]["RimColor"] = shading.rim_light.color
            if layers:
                if layers.curvature.enabled:
                    params["ScalarParameterValues"]["CurvatureIntensity"] = layers.curvature.intensity
                if layers.grunge.enabled:
                    params["ScalarParameterValues"]["GrungeIntensity"] = layers.grunge.intensity
        return params
