class UnrealAnimationExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        anim_graph = character.metadata.get("animation_graph")
        if anim_graph:
            base_clip_id = anim_graph.get("base_clip_id", "idle")
            manifest.assets.animations.append(f"{base_clip_id}.fbx")
