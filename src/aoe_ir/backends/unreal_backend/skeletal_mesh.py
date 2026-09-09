class UnrealSkeletalMeshExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        base_mesh = character.metadata.get("base_mesh", "fallback.fbx")
        manifest.source_files[f"SK_{getattr(character, 'character_id', getattr(character, 'asset_id', 'Unknown'))}"] = base_mesh
