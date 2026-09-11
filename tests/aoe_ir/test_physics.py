import unittest
from src.aoe_ir.physics import PhysicsRigIR, SecondaryMotionProfileIR, PhysicsColliderIR, ColliderType

class TestPhysicsIR(unittest.TestCase):
    def test_physics_rig_definition(self):
        rig = PhysicsRigIR()

        # Add colliders for body
        rig.colliders.append(PhysicsColliderIR(collider_id="head_col", bone_parent="head", type=ColliderType.SPHERE, radius=0.2))
        rig.colliders.append(PhysicsColliderIR(collider_id="arm_col", bone_parent="upper_arm_L", type=ColliderType.CAPSULE, radius=0.1, length=0.4))

        # Add physics simulation (spring/jiggle) for hair and clothes
        rig.secondary_motion.append(SecondaryMotionProfileIR(chain_root="hair_front", stiffness=0.2, damping=0.1, wind_influence=1.5))
        rig.secondary_motion.append(SecondaryMotionProfileIR(chain_root="skirt_root", stiffness=0.8, damping=0.5, gravity_multiplier=1.2))

        self.assertEqual(len(rig.colliders), 2)
        self.assertEqual(len(rig.secondary_motion), 2)
        self.assertEqual(rig.secondary_motion[0].wind_influence, 1.5)
        self.assertEqual(rig.colliders[1].type, ColliderType.CAPSULE)

if __name__ == '__main__':
    unittest.main()
