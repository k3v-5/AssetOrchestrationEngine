class UnrealSequencerExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        anim_graph_dict = character.metadata.get("animation_graph")
        if not anim_graph_dict:
            return

        expressions = []
        if "facial_tracks" in anim_graph_dict:
            for track_id, track_data in anim_graph_dict["facial_tracks"].items():
                for keyframe, morphs in track_data.get("keyframes", {}).items():
                    for morph_name, value in morphs.items():
                        expressions.append({
                            "morph_target": morph_name,
                            "time": keyframe,
                            "value": value
                        })

        manifest.expressions["morphs"] = expressions
