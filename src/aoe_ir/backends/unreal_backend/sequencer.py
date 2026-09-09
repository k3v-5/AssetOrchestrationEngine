from .manifest import MorphTargetInfo

class UnrealSequencerExporter:
    @staticmethod
    def plan_export(character, manifest, output_dir: str):
        anim_graph_dict = character.metadata.get("animation_graph")
        if not anim_graph_dict:
            return

        if "facial_tracks" in anim_graph_dict:
            for track_id, track_data in anim_graph_dict["facial_tracks"].items():
                for keyframe, morphs in track_data.get("keyframes", {}).items():
                    for morph_name, value in morphs.items():
                        manifest.morph_targets.append(MorphTargetInfo(
                            name=morph_name,
                            time=keyframe,
                            value=value
                        ))
