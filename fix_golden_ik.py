with open("tests/integration/blender/test_retargeting_golden.py", "r") as f:
    code = f.read()

import_str = "from src.aoe_ir.animation import AnimationFoundationIR, InterpolationType"
new_import = "from src.aoe_ir.animation import AnimationFoundationIR, InterpolationType\nfrom src.aoe_ir.ik import IKSolverConfigIR, IKConstraintIR, IKConstraintType"
code = code.replace(import_str, new_import)

old_test = """                char.animation.clips["walk"] = aoe_clip
                char.animation.active_clip = "walk"

                render_base_path = os.path.join(tmpdir, f"retarget_{style_name.lower()}.png")"""

new_test = """                char.animation.clips["walk"] = aoe_clip
                char.animation.active_clip = "walk"

                # Apply an IK constraint to the feet pointing to the floor
                char.ik_config = IKSolverConfigIR(
                    solver_id="legs",
                    constraints=[
                        IKConstraintIR(
                            constraint_id="foot_l_plant",
                            bone_target="foot_L",
                            constraint_type=IKConstraintType.POSITION,
                            chain_length=2,
                            target_position=(0.1, 0, 0)
                        ),
                        IKConstraintIR(
                            constraint_id="foot_r_plant",
                            bone_target="foot_R",
                            constraint_type=IKConstraintType.POSITION,
                            chain_length=2,
                            target_position=(-0.1, 0, 0)
                        )
                    ]
                )

                render_base_path = os.path.join(tmpdir, f"retarget_{style_name.lower()}.png")"""

code = code.replace(old_test, new_test)

with open("tests/integration/blender/test_retargeting_golden.py", "w") as f:
    f.write(code)
