from .animation import ExternalAnimation
from .mapper import SkeletonMapConfig
from ..animation import AnimationClipIR
from ..pose import PoseIR, PoseTransformIR
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

@dataclass
class RetargetProfileIR:
    profile_id: str
    skeleton_map: SkeletonMapConfig
    global_scale: float = 1.0
    preserve_root_motion: bool = False
    rotation_offsets: Dict[str, Tuple[float, float, float]] = field(default_factory=dict)


class AnimationRetargeter:
    """Translates ExternalAnimation to AOE's internal AnimationClipIR via a SkeletonMapConfig."""

    @staticmethod
    def retarget(external_anim: ExternalAnimation, mapper_or_profile) -> AnimationClipIR:

        # Support old signature or new RetargetProfileIR
        if isinstance(mapper_or_profile, SkeletonMapConfig):
            profile = RetargetProfileIR("legacy", mapper_or_profile)
        else:
            profile = mapper_or_profile

        mapper = profile.skeleton_map

        clip_ir = AnimationClipIR(
            clip_id=external_anim.animation_id,
            duration_frames=external_anim.duration_frames,
            fps=external_anim.fps,
            is_looping=True # Default for simple retargeting assumption
        )

        for ext_kf in external_anim.keyframes:
            pose = PoseIR(pose_id=f"frame_{ext_kf.frame}")

            for ext_bone_id, ext_transform in ext_kf.transforms.items():
                # Map bone
                if ext_bone_id in mapper.bone_map:
                    aoe_bone_id = mapper.bone_map[ext_bone_id]

                    rot = list(ext_transform.rotation_euler)

                    # Apply offsets if any exist in the profile
                    if aoe_bone_id in profile.rotation_offsets:
                        offset = profile.rotation_offsets[aoe_bone_id]
                        rot[0] += offset[0]
                        rot[1] += offset[1]
                        rot[2] += offset[2]

                    loc = list(ext_transform.location)
                    loc[0] *= profile.global_scale
                    loc[1] *= profile.global_scale
                    loc[2] *= profile.global_scale

                    pose.bone_transforms[aoe_bone_id] = PoseTransformIR(
                        location=tuple(loc),
                        rotation_euler=tuple(rot)
                    )

            clip_ir.keyframes[ext_kf.frame] = pose

        return clip_ir
