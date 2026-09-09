from .manifest import PhysicsNodeInfo

class UnrealAnimBlueprintExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        if getattr(character, "physics_rig", None):
            for sec in character.physics_rig.secondary_motion:
                # Default to AnimDynamics unless overridden
                phys_type = getattr(sec, 'physics_type', 'AnimDynamics')
                manifest.physics_nodes.append(PhysicsNodeInfo(
                    bone_target=sec.chain_root,
                    physics_type=phys_type,
                    stiffness=sec.stiffness,
                    damping=sec.damping
                ))
