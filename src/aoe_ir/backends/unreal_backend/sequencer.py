class UnrealSequencerExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        anim_graph_dict = character.metadata.get("animation_graph")
        if not anim_graph_dict:
            return

        seq_name = f"LS_{getattr(character, 'character_id', getattr(character, 'asset_id', 'Unknown'))}_Cinematic"
        tracks = []

        base_clip_id = anim_graph_dict.get("base_clip_id", "idle")
        tracks.append({
            "track_type": "SkeletalAnimationTrack",
            "animation": f"Anim_{getattr(character, 'character_id', getattr(character, 'asset_id', 'Unknown'))}_{base_clip_id}"
        })

        if "facial_tracks" in anim_graph_dict:
            for track_id, track_data in anim_graph_dict["facial_tracks"].items():
                for keyframe, morphs in track_data.get("keyframes", {}).items():
                    for morph_name, value in morphs.items():
                        tracks.append({
                            "track_type": "FloatCurveTrack",
                            "target_property": f"MorphTarget:{morph_name}",
                            "keys": [{"time": keyframe, "value": value}]
                        })

        manifest.metadata["level_sequence"] = {
            "sequence_name": seq_name,
            "tracks": tracks
        }
