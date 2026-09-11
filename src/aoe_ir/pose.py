from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class TransformIR:
    location: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation_euler: Tuple[float, float, float] = (0.0, 0.0, 0.0) # XYZ
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)

@dataclass
class PoseTransformIR(TransformIR):
    # Backward compatibility wrapper / clarity alias for bone-specific transforms
    pass

@dataclass
class PoseIR:
    pose_id: str
    bone_transforms: Dict[str, PoseTransformIR] = field(default_factory=dict)
