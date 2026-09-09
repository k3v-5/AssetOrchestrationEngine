from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class SkeletonMapConfig:
    """Configuration mapping external skeleton bone names to AOE SkeletonIR bone names."""
    mapping_name: str
    bone_map: Dict[str, str] = field(default_factory=dict) # external_name -> aoe_name

    # Optional offsets for fixing T-Pose/A-Pose differences
    rotation_offsets: Dict[str, tuple] = field(default_factory=dict)

class SkeletonMapper:
    """Maps external bones to internal SkeletonIR representation."""

    @staticmethod
    def create_mixamo_mapper() -> SkeletonMapConfig:
        """Factory for a common Mixamo to AOE Minimal Humanoid mapper."""
        return SkeletonMapConfig(
            mapping_name="MixamoToAOE",
            bone_map={
                "mixamorig:Hips": "pelvis",
                "mixamorig:Spine": "spine",
                "mixamorig:Neck": "neck",
                "mixamorig:Head": "head",
                "mixamorig:LeftShoulder": "clavicle_L",
                "mixamorig:LeftArm": "upper_arm_L",
                "mixamorig:LeftForeArm": "forearm_L",
                "mixamorig:LeftHand": "hand_L",
                "mixamorig:RightShoulder": "clavicle_R",
                "mixamorig:RightArm": "upper_arm_R",
                "mixamorig:RightForeArm": "forearm_R",
                "mixamorig:RightHand": "hand_R",
                "mixamorig:LeftUpLeg": "thigh_L",
                "mixamorig:LeftLeg": "shin_L",
                "mixamorig:LeftFoot": "foot_L",
                "mixamorig:RightUpLeg": "thigh_R",
                "mixamorig:RightLeg": "shin_R",
                "mixamorig:RightFoot": "foot_R"
            }
        )
