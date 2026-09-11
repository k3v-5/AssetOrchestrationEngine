from typing import List
from ..animation import AnimationFoundationIR

class AnimationValidationResult:
    def __init__(self, is_valid: bool, issues: List[str]):
        self.is_valid = is_valid
        self.issues = issues

class AnimationValidator:

    @staticmethod
    def validate(animation: AnimationFoundationIR) -> AnimationValidationResult:
        issues = []

        if not animation.rest_pose:
            issues.append("AnimationFoundationIR requires a defined rest_pose.")

        for clip_id, clip in animation.clips.items():
            if clip.duration_frames <= 0:
                issues.append(f"Clip '{clip_id}' must have duration_frames > 0.")
            if clip.fps <= 0:
                issues.append(f"Clip '{clip_id}' must have fps > 0.")

            for frame_idx, pose in clip.keyframes.items():
                # For continuous time we might allow keys slightly outside but strictly positive
                if frame_idx < 0:
                    issues.append(f"Clip '{clip_id}' has negative frame index {frame_idx}.")
                if frame_idx > clip.duration_frames:
                    issues.append(f"Clip '{clip_id}' keyframe {frame_idx} exceeds duration {clip.duration_frames}.")

        return AnimationValidationResult(len(issues) == 0, issues)
