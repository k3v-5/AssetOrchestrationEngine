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
class CurvatureLayerIR:
    enabled: bool = False
    intensity: float = 1.0
    edge_color: str = "#000000"
    cavity_color: str = "#111111"
    blend_mode: str = "MULTIPLY"

@dataclass
class GrungeLayerIR:
    enabled: bool = False
    intensity: float = 1.0
    scale: float = 10.0
    color: str = "#222222"
    blend_mode: str = "MULTIPLY"
    # Determines if grunge is driven by AO, cavity, or flat procedural noise
    driver: str = "CAVITY"

@dataclass
class HatchingLayerIR:
    enabled: bool = False
    intensity: float = 1.0
    scale: float = 5.0
    color: str = "#000000"
    rotation_angle: float = 45.0
    # Object, Screen, World, or Tangent
    coordinate_space: str = "SCREEN"
    blend_mode: str = "MULTIPLY"

@dataclass
class TemporalBehaviorIR:
    enabled: bool = False
    update_rate: int = 2 # Change noise every N frames
    hold_frames: int = 1 # How long a generated texture holds before flipping
    transition_mode: str = "SNAP" # SNAP or BLEND
    seed_offset: int = 0

@dataclass
class StyleLayerIR:
    curvature: CurvatureLayerIR = field(default_factory=CurvatureLayerIR)
    grunge: GrungeLayerIR = field(default_factory=GrungeLayerIR)
    hatching: HatchingLayerIR = field(default_factory=HatchingLayerIR)
    temporal: TemporalBehaviorIR = field(default_factory=TemporalBehaviorIR)

@dataclass
class NPRProfileIR:
    shading: ShadingProfile = field(default_factory=ShadingProfile)
    outline: OutlineProfile = field(default_factory=OutlineProfile)
    layers: StyleLayerIR = field(default_factory=StyleLayerIR)

@dataclass
class StyleProfile:
    style_type: StyleProfileType = StyleProfileType.REALISTIC

    # Base configuration backwards compatible
    shading: ShadingProfile = field(default_factory=ShadingProfile)
    outline: OutlineProfile = field(default_factory=OutlineProfile)
    texture: TextureProfile = field(default_factory=TextureProfile)

    # Advanced composition
    npr_profile: Optional[NPRProfileIR] = None

    parameters: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AppearanceProfile:
    appearance_id: str
    family: AppearanceFamily = AppearanceFamily.PBR
    style: StyleProfile = field(default_factory=StyleProfile)
    # Allows overriding style per semantic region (e.g. "face", "hair")
    region_overrides: Dict[str, StyleProfile] = field(default_factory=dict)
    parameters: Dict[str, Any] = field(default_factory=dict)
