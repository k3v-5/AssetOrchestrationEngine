class UnrealSkeletalMeshExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        base_mesh = character.metadata.get("base_mesh", "fallback.fbx")
        manifest.assets.meshes.append(base_mesh)
