import unittest
from src.aoe_ir.ik import IKConstraintIR, IKConstraintType, IKSolverConfigIR

class TestIKIR(unittest.TestCase):
    def test_ik_constraint_structure(self):
        foot_ik = IKConstraintIR(
            constraint_id="foot_L_ik",
            bone_target="foot_L",
            constraint_type=IKConstraintType.TRANSFORM,
            target_position=(0, 0, 0), # Planted on floor
            chain_length=2 # foot -> shin -> thigh
        )

        solver = IKSolverConfigIR(
            solver_id="humanoid_legs",
            constraints=[foot_ik]
        )

        self.assertEqual(solver.constraints[0].bone_target, "foot_L")
        self.assertEqual(solver.constraints[0].chain_length, 2)
        self.assertEqual(solver.constraints[0].target_position, (0, 0, 0))

if __name__ == "__main__":
    unittest.main()

from src.aoe_ir.skeleton import SkeletonIR, BoneIR
from src.aoe_ir.validation.ik_validator import IKValidator

class TestIKValidator(unittest.TestCase):
    def setUp(self):
        self.skeleton = SkeletonIR(
            skeleton_id="humanoid",
            bones={
                "root": BoneIR("root"),
                "pelvis": BoneIR("pelvis", parent="root"),
                "thigh": BoneIR("thigh", parent="pelvis"),
                "shin": BoneIR("shin", parent="thigh"),
                "foot": BoneIR("foot", parent="shin")
            }
        )

    def test_ik_validator_success(self):
        ik = IKSolverConfigIR(
            solver_id="legs",
            constraints=[
                IKConstraintIR(
                    constraint_id="foot_ik",
                    bone_target="foot",
                    constraint_type=IKConstraintType.POSITION,
                    chain_length=3 # foot -> shin -> thigh
                )
            ]
        )
        res = IKValidator.validate(ik, self.skeleton)
        self.assertTrue(res.is_valid)

    def test_ik_validator_fail_hierarchy_depth(self):
        ik = IKSolverConfigIR(
            solver_id="legs",
            constraints=[
                IKConstraintIR(
                    constraint_id="foot_ik",
                    bone_target="foot",
                    constraint_type=IKConstraintType.POSITION,
                    chain_length=6 # Exceeds root (depth 5 max)
                )
            ]
        )
        res = IKValidator.validate(ik, self.skeleton)
        self.assertFalse(res.is_valid)
        self.assertIn("exceeds hierarchy depth", res.issues[0])
