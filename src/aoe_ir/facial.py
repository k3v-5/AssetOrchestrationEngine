from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

@dataclass
class BlendShapeIR:
    """Represents a target morph/shape delta independent of implementation."""
    shape_id: str
    mesh_id: str
    name: str
    # Conceptual delta information could go here, but generally
    # the backend implements this via existing Shape Keys/Morph Targets.
    # This acts as the contract signature.
    weight_range: tuple = (0.0, 1.0)

class FacialChannelType(str, Enum):
    BLENDSHAPE = "BLENDSHAPE"
    BONE = "BONE"
    MATERIAL_PARAM = "MATERIAL_PARAM"
    TEXTURE_SWAP = "TEXTURE_SWAP"

@dataclass
class ExpressionComponentIR:
    """A scalar value applied to a specific facial channel."""
    channel_id: str
    channel_type: FacialChannelType = FacialChannelType.BLENDSHAPE
    weight: float = 1.0

@dataclass
class ExpressionProfileIR:
    """A semantic expression composed of multiple channels (e.g., Smile)."""
    expression_id: str
    components: List[ExpressionComponentIR] = field(default_factory=list)

@dataclass
class FaceRigIR:
    """The central facial controller connecting shapes and bones to semantics."""
    rig_id: str
    blend_shapes: Dict[str, BlendShapeIR] = field(default_factory=dict)
    expressions: Dict[str, ExpressionProfileIR] = field(default_factory=dict)

@dataclass
class PhonemeEventIR:
    """A specific phoneme triggered at a timestamp."""
    time: float
    phoneme: str # e.g., 'A', 'O', 'M', 'SIL'
    weight: float = 1.0

@dataclass
class LipSyncTrackIR:
    """A timeline of phonemes extracted from audio or external JSON."""
    track_id: str
    phonemes: List[PhonemeEventIR] = field(default_factory=list)

@dataclass
class VisemeMappingIR:
    """Maps semantic phonemes to Expression Profiles."""
    viseme_id: str
    expression_id: str # Target ExpressionProfileIR
    phoneme_triggers: List[str] = field(default_factory=list) # e.g., ['A', 'E', 'I']

@dataclass
class ExpressionTrackIR:
    """A timeline tracking the intensity of expressions."""
    track_id: str
    keyframes: Dict[int, Dict[str, float]] = field(default_factory=dict) # frame -> {expression_id -> weight}
