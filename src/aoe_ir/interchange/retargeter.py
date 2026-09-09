from .animation import ExternalAnimation
from .mapper import SkeletonMapConfig
from ..animation import AnimationClipIR
from ..pose import PoseIR, PoseTransformIR

class AnimationRetargeter:
    """Translates ExternalAnimation to AOE's internal AnimationClipIR via a SkeletonMapConfig."""

    @staticmethod
    def retarget(external_anim: ExternalAnimation, mapper: SkeletonMapConfig) -> AnimationClipIR:
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

                    # Optional offset logic would go here if defined in mapper.rotation_offsets

                    pose.bone_transforms[aoe_bone_id] = PoseTransformIR(
                        location=ext_transform.location,
                        rotation_euler=ext_transform.rotation_euler
                    )

            clip_ir.keyframes[ext_kf.frame] = pose

        return clip_ir
