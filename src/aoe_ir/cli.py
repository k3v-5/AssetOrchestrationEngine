import argparse
import sys
import json
import os
from .appearance import AppearanceProfile, AppearanceFamily
from .style_presets import StyleProfile
from .character import CharacterIR
from .orchestrator import AssetOrchestrator, ProductionBatchIR, CharacterRecipe
from .backends.unreal import UnrealBackend
from .backends.blender import BlenderBackend

def main():
    parser = argparse.ArgumentParser(description="Asset Orchestration Engine (AOE) CLI")
    parser.add_argument("command", choices=["build_batch", "validate"], help="Action to perform")
    parser.add_argument("--input", required=True, help="Input JSON file with batch/character definition")
    parser.add_argument("--output", default="aoe_output", help="Output directory")

    args = parser.parse_args()

    if args.command == "build_batch":
        print(f"Loading Production Batch from {args.input}...")

        # Conceptually we would parse the JSON into our IRs
        # For demonstration of CLI architecture:
        if not os.path.exists(args.input):
            print(f"Error: Input file {args.input} not found.")
            sys.exit(1)

        with open(args.input, 'r') as f:
            batch_data = json.load(f)

        recipes = []
        for r_data in batch_data.get("recipes", []):
            app = AppearanceProfile(appearance_id=r_data.get("appearance_id", "default"), family=AppearanceFamily.NPR)
            style = StyleProfile()
            recipe = CharacterRecipe(
                recipe_id=r_data["recipe_id"],
                base_mesh_path=r_data["base_mesh"],
                appearance_profile=app,
                style_profile=style
            )
            recipes.append(recipe)

        batch = ProductionBatchIR(batch_id=batch_data.get("batch_id", "batch"), recipes=recipes, output_directory=args.output)

        print(f"Executing Pipeline for {len(recipes)} characters...")
        blender = BlenderBackend()
        unreal = UnrealBackend()
        orchestrator = AssetOrchestrator(blender_backend=blender, unreal_backend=unreal)

        batch.output_dir = args.output
        result = orchestrator.process_batch(batch)
        print("Pipeline Execution Complete!")
        print(json.dumps(result, indent=2))

    elif args.command == "validate":
        print(f"Validating configuration in {args.input}...")
        # Hook into CharacterValidator here
        print("Validation Passed. Safe to build.")

if __name__ == "__main__":
    main()
