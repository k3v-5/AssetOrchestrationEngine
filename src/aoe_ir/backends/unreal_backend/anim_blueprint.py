class UnrealAnimBlueprintExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        anim_graph_dict = character.metadata.get("animation_graph")
        if not anim_graph_dict:
            return

        anim_dynamics = []
        if getattr(character, "physics_rig", None):
            for sec in character.physics_rig.secondary_motion:
                anim_dynamics.append({
                    "bone_chain": sec.chain_root,
                    "stiffness": sec.stiffness,
                    "damping": sec.damping
                })

        manifest.physics["anim_dynamics"] = anim_dynamics
