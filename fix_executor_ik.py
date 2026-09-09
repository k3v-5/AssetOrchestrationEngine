with open("tests/integration/blender/executor.py", "r") as f:
    code = f.read()

# Add logic for IK configuration mapping
ik_logic = """
        # Apply IK Constraints if present
        ik_config = asset.get("ik_config", {})
        if ik_config and armature:
            bpy.ops.object.mode_set(mode='POSE')
            for constraint in ik_config.get("constraints", []):
                bone_target = constraint.get("bone_target")
                if bone_target and bone_target in armature.pose.bones:
                    pbone = armature.pose.bones[bone_target]
                    c_type = constraint.get("constraint_type", "POSITION")

                    if c_type == "POSITION" or c_type == "TRANSFORM":
                        # Create IK Constraint in Blender
                        ik = pbone.constraints.new('IK')
                        ik.chain_count = constraint.get("chain_length", 1)
                        # Normally we would set a target object or empty here.
                        # For headless testing, if no target object is provided, we just add the constraint.
                        if constraint.get("target_position"):
                            # We create an Empty as target
                            bpy.ops.object.mode_set(mode='OBJECT')
                            bpy.ops.object.empty_add(type='PLAIN_AXES', location=constraint.get("target_position"))
                            target_obj = bpy.context.active_object
                            target_obj.name = f"IK_Target_{bone_target}"

                            bpy.ops.object.select_all(action='DESELECT')
                            armature.select_set(True)
                            bpy.context.view_layer.objects.active = armature
                            bpy.ops.object.mode_set(mode='POSE')

                            ik.target = target_obj
                            logging.info(f"Assigned IK Constraint for {bone_target} with target {target_obj.name}")
            bpy.ops.object.mode_set(mode='OBJECT')
"""

# Insert IK logic after Animation loading
old_anim_block = """            # If we just need a static pose
            if not active_clip_id:"""

code = code.replace(old_anim_block, ik_logic + "\n" + old_anim_block)

with open("tests/integration/blender/executor.py", "w") as f:
    f.write(code)
