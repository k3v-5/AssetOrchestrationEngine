from typing import List, Dict, Any
from ..appearance import AppearanceProfile, AppearanceFamily, ShaderModel

class ValidationResult:
    def __init__(self, is_valid: bool, issues: List[str]):
        self.is_valid = is_valid
        self.issues = issues

class AppearanceValidator:
    """Agnostic validator that applies different rules based on the Appearance Family."""

    @staticmethod
    def validate(profile: AppearanceProfile) -> ValidationResult:
        if profile.family == AppearanceFamily.PBR:
            return AppearanceValidator._validate_pbr(profile)
        elif profile.family == AppearanceFamily.NPR:
            return AppearanceValidator._validate_npr(profile)

        return ValidationResult(True, [])

    @staticmethod
    def _validate_pbr(profile: AppearanceProfile) -> ValidationResult:
        issues = []
        if profile.style.shading.model != ShaderModel.PBR:
            issues.append(f"PBR family expects PBR shading model, got {profile.style.shading.model.name}")

        if profile.style.outline.enabled:
            issues.append("PBR family does not support outline rendering natively")

        return ValidationResult(len(issues) == 0, issues)

    @staticmethod
    def _validate_npr(profile: AppearanceProfile) -> ValidationResult:
        issues = []
        if profile.style.shading.model == ShaderModel.PBR:
            issues.append("NPR family expects non-PBR shading models (e.g. TOON, UNLIT)")

        if profile.style.shading.model == ShaderModel.TOON:
            if profile.style.shading.band_count < 1:
                issues.append("TOON shading requires at least 1 color band")

        return ValidationResult(len(issues) == 0, issues)
