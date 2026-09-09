class UnrealProjectOrchestrator:
    @staticmethod
    def generate_import_script(manifest_path: str, output_script_path: str):
        script_content = f"""# UE5 Generated Import Script for AOE
import unreal
import json

def run_import():
    manifest_path = r"{manifest_path}"

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    char_id = manifest.get('manifest_id', 'Unknown')
    print(f"Starting Zero-Click Integration for AOE Manifest: {{char_id}}")

    # 1. Setup Folders
    base_path = f"/Game/AOE_Imports/{{char_id}}"
    unreal.EditorAssetLibrary.make_directory(base_path)

    # 2. Materials
    # In UE5 Python API, material instances can be created using AssetTools
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_factory = unreal.MaterialInstanceConstantFactoryNew()

    for mat_name, mat_data in manifest.get("material_instances", {{}}).items():
        print(f"Creating Material Instance: {{mat_name}}")
        mi = asset_tools.create_asset(mat_name, f"{{base_path}}/Materials", unreal.MaterialInstanceConstant, material_factory)
        master_mat = unreal.EditorAssetLibrary.load_asset(mat_data["master_material"])
        unreal.MaterialEditingLibrary.set_material_instance_parent(mi, master_mat)

        # Apply Scalar parameters
        for param_name, param_val in mat_data.get("parameters", {{}}).get("ScalarParameterValues", {{}}).items():
            unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi, param_name, param_val)

        # Apply Vector parameters
        for param_name, param_val in mat_data.get("parameters", {{}}).get("VectorParameterValues", {{}}).items():
            linear_color = hex_to_linear(param_val)
            unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi, param_name, linear_color)

    # 3. Meshes & Animations
    for asset_name, source_path in manifest.get("source_files", {{}}).items():
        print(f"Importing FBX: {{asset_name}} from {{source_path}}")
        import_task = unreal.AssetImportTask()
        import_task.filename = source_path
        import_task.destination_path = base_path
        import_task.automated = True
        import_task.replace_existing = True
        import_task.save = True

        options = unreal.FbxImportUI()
        options.import_mesh = True
        options.import_as_skeletal = True
        options.import_materials = False
        import_task.options = options

        asset_tools.import_asset_tasks([import_task])

    # 4. Blueprints and Sequences
    if "metadata" in manifest:
        if "anim_blueprint" in manifest["metadata"]:
            print(f"Configuring Anim Blueprint: {{manifest['metadata']['anim_blueprint']['asset_name']}}")
        if "level_sequence" in manifest["metadata"]:
            print(f"Configuring Level Sequence: {{manifest['metadata']['level_sequence']['sequence_name']}}")

    print("Zero-Click Integration Complete.")

if __name__ == "__main__":
    run_import()
"""
        with open(output_script_path, 'w') as f:
            f.write(script_content)
