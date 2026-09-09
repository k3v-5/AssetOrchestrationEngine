from dataclasses import dataclass, field
from typing import Dict, List, Any
from enum import Enum

class ColliderType(str, Enum):
    SPHERE = "SPHERE"
    CAPSULE = "CAPSULE"
    BOX = "BOX"

@dataclass
class PhysicsColliderIR:
    collider_id: str
    bone_parent: str
    type: ColliderType
    radius: float = 0.1
    length: float = 0.5
    offset: List[float] = field(default_factory=lambda: [0, 0, 0])

@dataclass
class SecondaryMotionProfileIR:
    """Defines simulation parameters for things like hair, cloth, jiggle."""
    chain_root: str
    stiffness: float = 0.5
    damping: float = 0.2
    gravity_multiplier: float = 1.0
    mass: float = 1.0
    wind_influence: float = 0.0

@dataclass
class PhysicsRigIR:
    """The complete physical definition of the character."""
    colliders: List[PhysicsColliderIR] = field(default_factory=list)
    secondary_motion: List[SecondaryMotionProfileIR] = field(default_factory=list)
