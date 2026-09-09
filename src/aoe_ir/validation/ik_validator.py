from typing import List
from ..ik import IKSolverConfigIR
from ..skeleton import SkeletonIR

class IKValidationResult:
    def __init__(self, is_valid: bool, issues: List[str]):
        self.is_valid = is_valid
        self.issues = issues

class IKValidator:

    @staticmethod
    def validate(ik_config: IKSolverConfigIR, skeleton: SkeletonIR) -> IKValidationResult:
        issues = []

        bone_names = set(skeleton.bones.keys())

        for constraint in ik_config.constraints:
            if constraint.bone_target not in bone_names:
                issues.append(f"IK Constraint '{constraint.constraint_id}' targets unknown bone '{constraint.bone_target}'")

            if constraint.chain_length < 0:
                issues.append(f"IK Constraint '{constraint.constraint_id}' has invalid chain length {constraint.chain_length}")

            if constraint.chain_length > 0:
                # Walk up the hierarchy to ensure chain length is valid
                current_bone = constraint.bone_target
                length = 0
                while current_bone and length < constraint.chain_length:
                    bone_obj = skeleton.bones.get(current_bone)
                    if not bone_obj:
                        break
                    current_bone = bone_obj.parent
                    length += 1

                if length < constraint.chain_length:
                    issues.append(f"IK Constraint '{constraint.constraint_id}' chain length {constraint.chain_length} exceeds hierarchy depth (max {length})")

        return IKValidationResult(len(issues) == 0, issues)
