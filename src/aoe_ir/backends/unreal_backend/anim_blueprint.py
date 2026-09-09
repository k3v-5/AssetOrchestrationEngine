class UnrealAnimBlueprintExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        anim_graph_dict = character.metadata.get("animation_graph")
        if not anim_graph_dict:
            return

        abp_name = f"ABP_{getattr(character, 'character_id', getattr(character, 'asset_id', 'Unknown'))}"
        state_machine = {"name": "Locomotion", "states": []}

        base_clip_id = anim_graph_dict.get("base_clip_id", "idle")
        state_machine["states"].append({
            "state_name": "BaseState",
            "sequence": f"Anim_{getattr(character, 'character_id', getattr(character, 'asset_id', 'Unknown'))}_{base_clip_id}"
        })

        layered_blends = []
        if "facial_tracks" in anim_graph_dict:
            for track_id in anim_graph_dict["facial_tracks"].keys():
                layered_blends.append({
                    "layer_name": track_id,
                    "blend_type": "LayeredBlendPerBone",
                    "bone_filter": "neck"
                })

        control_rig_hooks = []
        if getattr(character, "ik_config", None):
            for constraint in character.ik_config.constraints:
                control_rig_hooks.append({
                    "effector_bone": constraint.bone_target,
                    "type": constraint.constraint_type.value,
                    "ik_node": "FullBodyIK" if constraint.chain_length > 2 else "BasicIK"
                })

        anim_dynamics = []
        if getattr(character, "physics_rig", None):
            for sec in character.physics_rig.secondary_motion:
                anim_dynamics.append({
                    "bone_chain": sec.chain_root,
                    "node_type": "KawaiiPhysics",
                    "stiffness": sec.stiffness,
                    "damping": sec.damping,
                    "wind": sec.wind_influence
                })

        abp_definition = {
            "asset_name": abp_name,
            "state_machine": state_machine,
            "layered_blends": layered_blends,
            "control_rigs": control_rig_hooks,
            "secondary_motion": anim_dynamics
        }

        manifest.metadata["anim_blueprint"] = abp_definition
