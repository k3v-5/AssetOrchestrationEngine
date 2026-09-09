import json
import os
from .manifest import UnrealAssetManifestIR, ManifestCharacterInfo, ManifestImportInfo
from .materials import UnrealMaterialTranslator
from .skeletal_mesh import UnrealSkeletalMeshExporter
from .animation import UnrealAnimationExporter
from .anim_blueprint import UnrealAnimBlueprintExporter
from .sequencer import UnrealSequencerExporter
from .project_orchestrator import UnrealProjectOrchestrator

class UnrealExporter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def export(self, character):
        os.makedirs(self.output_dir, exist_ok=True)
        char_id = getattr(character, "character_id", getattr(character, "asset_id", "Unknown"))

        manifest = UnrealAssetManifestIR()
        manifest.character = ManifestCharacterInfo(id=char_id)
        manifest.import_config = ManifestImportInfo(destination_root=f"/Game/AOE/{char_id}")

        material_info = UnrealMaterialTranslator.generate_instance_parameters(character.appearance, char_id)
        manifest.materials.instances.append(material_info)

        UnrealSkeletalMeshExporter.plan_export(character, manifest, self.output_dir)
        UnrealAnimationExporter.plan_export(character, manifest, self.output_dir)
        UnrealAnimBlueprintExporter.plan_export(character, manifest, self.output_dir)
        UnrealSequencerExporter.plan_export(character, manifest, self.output_dir)

        manifest_path = os.path.join(self.output_dir, f"{char_id}_manifest.json")
        manifest.save_manifest(manifest_path)

        import_script_path = os.path.join(self.output_dir, "ue5_import_orchestrator.py")
        UnrealProjectOrchestrator.generate_import_script(manifest_path, import_script_path)

        return manifest_path
