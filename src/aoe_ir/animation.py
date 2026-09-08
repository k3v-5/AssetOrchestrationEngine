from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .pose import PoseIR

@dataclass
class AnimationClipIR:
    clip_id: str
    duration_frames: int
    fps: int = 30
    keyframes: Dict[int, PoseIR] = field(default_factory=dict) # frame -> Pose

@dataclass
class AnimationFoundationIR:
    """Minimal representation of animation foundation for a character."""
    rest_pose: PoseIR
    clips: Dict[str, AnimationClipIR] = field(default_factory=dict)
    active_pose: Optional[str] = None # For static rendering, a selected pose from clips
