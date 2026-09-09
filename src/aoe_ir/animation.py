from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
from .pose import PoseIR
from .facial import ExpressionTrackIR, LipSyncTrackIR

class InterpolationType(str, Enum):
    LINEAR = "LINEAR"
    BEZIER = "BEZIER"
    CONSTANT = "CONSTANT"


@dataclass
class AnimationClipIR:
    clip_id: str
    duration_frames: int
    fps: int = 30
    keyframes: Dict[int, PoseIR] = field(default_factory=dict) # frame -> Pose
    # Used to denote if the clip should loop conceptually
    is_looping: bool = False
    # Explicit interpolation curve between keyframes
    interpolation: InterpolationType = InterpolationType.BEZIER

@dataclass
class AnimationFoundationIR:
    """Minimal representation of animation foundation for a character."""
    rest_pose: PoseIR
    clips: Dict[str, AnimationClipIR] = field(default_factory=dict)
    active_pose: Optional[str] = None # For static rendering, a selected pose from clips
    active_clip: Optional[str] = None # For sequence rendering

@dataclass
class AnimationLayerIR:
    layer_id: str
    clip_id: str
    weight: float = 1.0
    blend_mode: str = "ADDITIVE" # or OVERRIDE

@dataclass
class AnimationGraphIR:
    graph_id: str
    base_clip_id: str
    layers: List[AnimationLayerIR] = field(default_factory=list)

    # Facial and speech tracks run in parallel to skeletal clips
    facial_tracks: Dict[str, ExpressionTrackIR] = field(default_factory=dict)
    lipsync_tracks: Dict[str, LipSyncTrackIR] = field(default_factory=dict)

    active_facial_track: Optional[str] = None
    active_lipsync_track: Optional[str] = None
