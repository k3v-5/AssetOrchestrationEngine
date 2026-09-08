# This script runs INSIDE Blender.
# It acts as the "Executor" receiving the abstract plan and applying it to bpy.
import bpy
import json
import os
import sys

def create_toon_basic_material(mat_name, shading_config):
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    # Clear default nodes
    for node in nodes:
        nodes.remove(node)

    # Setup TOON BASIC
    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled") # We use Principled to receive light
    shader_to_rgb = nodes.new("ShaderNodeShaderToRGB")
    color_ramp = nodes.new("ShaderNodeValToRGB")

    color_ramp.color_ramp.interpolation = 'CONSTANT'
    band_count = shading_config.get("band_count", 2)

    # Adjust bands
    while len(color_ramp.color_ramp.elements) < band_count:
        color_ramp.color_ramp.elements.new(0.5)

    threshold = shading_config.get("shadow_threshold", 0.5)
    if band_count >= 2:
        color_ramp.color_ramp.elements[0].position = 0.0
        # Hex color to RGBA (approx for test)
        color_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.3, 1.0) # Shadow Color
        color_ramp.color_ramp.elements[1].position = threshold
        color_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.9, 1.0) # Highlight Color

    # Links
    links.new(bsdf.outputs['BSDF'], shader_to_rgb.inputs['Shader'])
    links.new(shader_to_rgb.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], output.inputs['Surface'])

    return mat

def apply_inverted_hull(obj, outline_config):
    # Duplicate object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.duplicate()
    outline_obj = bpy.context.active_object
    outline_obj.name = f"{obj.name}_Outline"

    # Add Solidify modifier
    mod = outline_obj.modifiers.new(name="Outline_Solidify", type='SOLIDIFY')
    mod.thickness = outline_config.get("width", 0.015)
    mod.offset = 1.0 # Inflate outwards
    mod.use_flip_normals = True

    # Set material (Black Unlit)
    mat = bpy.data.materials.new(name="Mat_Outline")
    mat.use_nodes = True
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)

    out = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    emission = mat.node_tree.nodes.new("ShaderNodeEmission")
    emission.inputs['Color'].default_value = (0, 0, 0, 1) # Black

    mat.node_tree.links.new(emission.outputs['Emission'], out.inputs['Surface'])

    mat.blend_method = 'OPAQUE'
    mat.shadow_method = 'NONE'

    # Assign material
    if len(outline_obj.data.materials) == 0:
        outline_obj.data.materials.append(mat)
    else:
        outline_obj.data.materials[0] = mat

    return outline_obj

def apply_semantic_materials(obj, appearance, regions):
    # Setup vertex groups based on semantic regions
    if not obj.data.vertex_colors:
        obj.data.vertex_colors.new()

    for region_id, indices in regions.items():
        vg = obj.vertex_groups.new(name=region_id)
        vg.add(indices, 1.0, 'REPLACE')

    # Example logic: if "FACE" is overridden, create a specific material
    if "FACE" in appearance.get("region_overrides", {}) and "FACE" in regions:
        # Create face material and assign
        pass # Simplified for the executor skeleton

def main():
    args_str = os.environ.get("AOE_BLENDER_ARGS", "{}")
    args = json.loads(args_str)

    asset = args.get("asset", {})
    appearance = asset.get("appearance", {})
    family = appearance.get("family", "PBR")
    style = appearance.get("style", {})

    # 1. Create Base Geometry (Monkey/Suzanne as test base if not specified)
    bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = asset.get("asset_id", "AOE_Asset")

    # Apply Subdivision Surface for smoothness
    subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 2
    bpy.ops.object.modifier_apply(modifier="Subsurf")

    result_data = {
        "status": "SUCCESS",
        "objects": [obj.name],
        "materials": [],
        "modifiers": []
    }

    # 2. Shading setup
    if family == "NPR" and style.get("shading", {}).get("model") == "TOON":
        mat = create_toon_basic_material(f"Mat_{obj.name}_Toon", style.get("shading", {}))
        obj.data.materials.append(mat)
        result_data["materials"].append(mat.name)

    # 3. Outline setup
    outline_conf = style.get("outline", {})
    if family == "NPR" and outline_conf.get("enabled", False) and outline_conf.get("method") == "INVERTED_HULL":
        outline_obj = apply_inverted_hull(obj, outline_conf)
        result_data["objects"].append(outline_obj.name)

    # 4. Semantic Regions setup
    semantic_regions = asset.get("semantic_regions", {})
    if semantic_regions:
        apply_semantic_materials(obj, appearance, semantic_regions)

    # Render if path is provided
    render_path = args.get("render_path")
    if render_path:
        # Basic camera and light
        bpy.ops.object.camera_add(location=(0, -6, 1), rotation=(1.2, 0, 0))
        cam = bpy.context.active_object
        bpy.context.scene.camera = cam

        bpy.ops.object.light_add(type='SUN', location=(0, 0, 5), rotation=(0.5, 0.5, 0))

        bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types.SceneEEVEE, 'TAA_samples') else 'BLENDER_EEVEE'
        bpy.context.scene.render.filepath = render_path
        bpy.ops.render.render(write_still=True)

    # Save .blend
    filepath = args.get("filepath")
    if filepath:
        bpy.ops.wm.save_as_mainfile(filepath=filepath)

    print(f"AOE_RESULT:{json.dumps(result_data)}")

if __name__ == "__main__":
    main()
