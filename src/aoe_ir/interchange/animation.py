from dataclasses import dataclass, field
from typing import Dict, List, Tuple
from ..pose import PoseTransformIR

@dataclass
class ExternalBoneTransform:
    # We might have matrices or just pos/rot/scale from external files (like FBX)
    location: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation_euler: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    # Could include quaternions depending on the external source format

@dataclass
class ExternalKeyframe:
    frame: int
    transforms: Dict[str, ExternalBoneTransform] = field(default_factory=dict) # original_bone_name -> Transform

@dataclass
class ExternalAnimation:
    """Represents an animation imported from an external source (Mixamo, FBX, BVH)."""
    animation_id: str
    duration_frames: int
    fps: int = 30
    keyframes: List[ExternalKeyframe] = field(default_factory=list)
    source_format: str = "UNKNOWN"
