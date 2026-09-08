from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

class AppearanceFamily(str, Enum):
    PBR = "PBR"
    NPR = "NPR"
    HYBRID = "HYBRID"
    UNLIT = "UNLIT"

class ShaderModel(str, Enum):
    PBR = "PBR"
    TOON = "TOON"
    UNLIT = "UNLIT"
    CUSTOM = "CUSTOM"

class StyleProfileType(str, Enum):
    REALISTIC = "REALISTIC"
    ANIME = "ANIME"
    CARTOON = "CARTOON"
    COMIC = "COMIC"
    SKETCH = "SKETCH"
    STYLIZED = "STYLIZED"

class OutlineMethod(str, Enum):
    NONE = "NONE"
    INVERTED_HULL = "INVERTED_HULL"
    POST_PROCESS = "POST_PROCESS"
    GEOMETRY_LINES = "GEOMETRY_LINES"
    FREESTYLE = "FREESTYLE"
    CUSTOM = "CUSTOM"

@dataclass
class OutlineProfile:
    enabled: bool = False
    method: OutlineMethod = OutlineMethod.NONE
    width: float = 0.015
    color: str = "#000000"
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RimLightProfile:
    enabled: bool = False
    intensity: float = 1.0
    color: str = "#FFFFFF"
    softness: float = 0.1
    width: float = 0.5

@dataclass
class SpecularProfile:
    enabled: bool = False
    intensity: float = 0.5
    roughness: float = 0.1
    color: str = "#FFFFFF"

@dataclass
class ShadingProfile:
    model: ShaderModel = ShaderModel.PBR

    # Base lighting
    band_count: int = 1
    shadow_softness: float = 0.0
    shadow_threshold: float = 0.5

    # Colors
    shadow_color: str = "#33334c"
    midtone_color: str = "#808099"
    highlight_color: str = "#ffffff"

    # Advanced Components
    rim_light: RimLightProfile = field(default_factory=RimLightProfile)
    specular: SpecularProfile = field(default_factory=SpecularProfile)

    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TextureProfile:
    mode: str = "PBR_MAPS" # PBR_MAPS, PAINTED, PROCEDURAL
    use_curvature: bool = False
    use_grunge: bool = False
    use_hatching: bool = False
    paint_variation: str = "NONE" # NONE, LOW, HIGH
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StyleProfile:
    style_type: StyleProfileType = StyleProfileType.REALISTIC
    shading: ShadingProfile = field(default_factory=ShadingProfile)
    outline: OutlineProfile = field(default_factory=OutlineProfile)
    texture: TextureProfile = field(default_factory=TextureProfile)
    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AppearanceProfile:
    appearance_id: str
    family: AppearanceFamily = AppearanceFamily.PBR
    style: StyleProfile = field(default_factory=StyleProfile)
    # Allows overriding style per semantic region (e.g. "face", "hair")
    region_overrides: Dict[str, StyleProfile] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
