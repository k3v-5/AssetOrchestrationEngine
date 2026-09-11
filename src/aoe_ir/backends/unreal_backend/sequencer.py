class UnrealSequencerExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        # We no longer iterate JSON keyframes.
        # We simply pass the baked FBX path if facial animation exists.
        anim_graph_dict = character.metadata.get("animation_graph")
        if anim_graph_dict and "facial_tracks" in anim_graph_dict:
            # Assuming Blender exported the facial curves to this path
            char_id = getattr(character, "character_id", getattr(character, "asset_id", "Unknown"))
            manifest.facial_animation_path = f"FacialAnim_{char_id}.fbx"
