from typing import List, Dict
from ..character import CharacterIR
import math

class CharacterValidationResult:
    def __init__(self, is_valid: bool, issues: List[str]):
        self.is_valid = is_valid
        self.issues = issues

class CharacterValidator:

    @staticmethod
    def validate(character: CharacterIR) -> CharacterValidationResult:
        issues = []

        # 1. Identity
        if not character.character_id:
            issues.append("Character has no identity (character_id).")

        # 2. Skeleton and Skinning checks
        if character.skeleton:
            bone_names = set(character.skeleton.bones.keys())

            for mesh_id, skinning in character.skinning.items():
                if mesh_id not in character.meshes:
                    issues.append(f"Skinning refers to unknown mesh '{mesh_id}'.")

                for vw in skinning.vertex_weights:
                    # Check max influences
                    if len(vw.weights) > skinning.max_influences:
                        issues.append(f"Vertex {vw.vertex_index} in mesh '{mesh_id}' exceeds max influences ({len(vw.weights)} > {skinning.max_influences}).")

                    total_weight = 0.0
                    for bone_name, weight in vw.weights.items():
                        # Check unknown bones
                        if bone_name not in bone_names:
                            issues.append(f"Vertex {vw.vertex_index} in mesh '{mesh_id}' references unknown bone '{bone_name}'.")

                        # Check valid weight range
                        if not (0.0 <= weight <= 1.0):
                            issues.append(f"Vertex {vw.vertex_index} in mesh '{mesh_id}' has invalid weight {weight} for bone '{bone_name}'.")

                        total_weight += weight

                    # Check weight normalization
                    if total_weight > 0 and not math.isclose(total_weight, 1.0, rel_tol=1e-5):
                        issues.append(f"Vertex {vw.vertex_index} in mesh '{mesh_id}' weights do not sum to 1.0 (Sum: {total_weight}).")

        return CharacterValidationResult(len(issues) == 0, issues)
