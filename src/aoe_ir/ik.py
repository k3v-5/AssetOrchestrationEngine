from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class IKConstraintType(str, Enum):
    POSITION = "POSITION"
    ROTATION = "ROTATION"
    TRANSFORM = "TRANSFORM" # Both pos and rot
    LOOK_AT = "LOOK_AT"
    POLE_VECTOR = "POLE_VECTOR"

@dataclass
class IKConstraintIR:
    constraint_id: str
    bone_target: str # The bone to constrain
    constraint_type: IKConstraintType

    # Target definition - either an external object/marker or a fixed world coordinate
    target_object_id: Optional[str] = None
    target_bone_id: Optional[str] = None # Or relative to another bone
    target_position: Optional[tuple] = None # (x, y, z)

    # IK Solver details
    chain_length: int = 1 # Number of bones to affect up the hierarchy
    weight: float = 1.0 # Blend weight of the IK effect
    pole_target_id: Optional[str] = None # e.g. for knee/elbow direction
    pole_angle: float = 0.0

@dataclass
class IKSolverConfigIR:
    """Configures multiple IK constraints acting on a skeleton."""
    solver_id: str
    constraints: List[IKConstraintIR] = field(default_factory=list)
