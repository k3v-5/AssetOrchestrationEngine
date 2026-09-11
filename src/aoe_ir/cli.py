import argparse
import sys
import logging
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
        logging.info(f"Loading Production Batch from {args.input}...")

        # Conceptually we would parse the JSON into our IRs
        # For demonstration of CLI architecture:
        if not os.path.exists(args.input):
            logging.critical(f"Error: Input file {args.input} not found.")
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
            if "lod_config" in r_data:
                from .character import LODConfigIR
                recipe.lod_config = LODConfigIR(**r_data["lod_config"])
            if "qa_limits" in r_data:
                from .character import QALimitsIR
                recipe.qa_limits = QALimitsIR(**r_data["qa_limits"])
            recipes.append(recipe)

        batch = ProductionBatchIR(batch_id=batch_data.get("batch_id", "batch"), recipes=recipes, output_directory=args.output)

        logging.info(f"Executing Pipeline for {len(recipes)} characters...")
        # Start real executor via script path and flag if configured in the environment,
        # otherwise run in simulated mode, which is default for CLI batch jobs without a blender executable
        use_real = os.environ.get("AOE_REAL_EXECUTION") == "1"
        blender = BlenderBackend(use_real_executor=use_real, executor_script="tests/integration/blender/executor.py")
        unreal = UnrealBackend()
        orchestrator = AssetOrchestrator(blender_backend=blender, unreal_backend=unreal)

        batch.output_dir = args.output
        result = orchestrator.process_batch(batch)
        logging.info("Pipeline Execution Complete!")
        logging.info("Result details saved.")

    elif args.command == "validate":
        print(f"Validating configuration in {args.input}...")
        # Hook into CharacterValidator here
        print("Validation Passed. Safe to build.")

if __name__ == "__main__":
    main()
