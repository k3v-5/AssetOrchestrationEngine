from .manifest import PhysicsNodeInfo

class UnrealAnimBlueprintExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        if getattr(character, "physics_rig", None):
            for sec in character.physics_rig.secondary_motion:
                phys_type = getattr(sec, 'physics_type', 'AnimDynamics')
                # Strict adherence: No magic numbers. If not provided by IR, passes None.
                stiff = getattr(sec, 'stiffness', None)
                damp = getattr(sec, 'damping', None)

                manifest.physics_nodes.append(PhysicsNodeInfo(
                    bone_target=sec.chain_root,
                    physics_type=phys_type,
                    stiffness=stiff,
                    damping=damp
                ))
