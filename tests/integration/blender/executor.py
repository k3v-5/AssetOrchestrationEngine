# This script runs INSIDE Blender.
# It acts as the "Executor" receiving the abstract plan and applying it to bpy.
import bpy
import json
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

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
    band_count = shading_config.get("band_count", 2) if isinstance(shading_config, dict) else 2

    # Adjust bands
    while len(color_ramp.color_ramp.elements) < band_count:
        color_ramp.color_ramp.elements.new(0.5)

    threshold = shading_config.get("shadow_threshold", 0.5) if isinstance(shading_config, dict) else 0.5

    # Simple distribution of bands based on count
    color_ramp.color_ramp.elements[0].position = 0.0
    color_ramp.color_ramp.elements[0].color = (0.1, 0.1, 0.2, 1.0) # Darkest Shadow

    if band_count == 2:
        color_ramp.color_ramp.elements[1].position = threshold
        color_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.9, 1.0) # Highlight
    elif band_count == 3:
        color_ramp.color_ramp.elements[1].position = threshold * 0.7
        color_ramp.color_ramp.elements[1].color = (0.4, 0.4, 0.5, 1.0) # Midtone
        color_ramp.color_ramp.elements[2].position = threshold * 1.3 if threshold * 1.3 <= 1.0 else 1.0
        color_ramp.color_ramp.elements[2].color = (0.9, 0.9, 1.0, 1.0) # Highlight
    elif band_count >= 4:
        color_ramp.color_ramp.elements[1].position = threshold * 0.5
        color_ramp.color_ramp.elements[1].color = (0.3, 0.3, 0.4, 1.0) # Core shadow
        color_ramp.color_ramp.elements[2].position = threshold
        color_ramp.color_ramp.elements[2].color = (0.6, 0.6, 0.7, 1.0) # Midtone
        color_ramp.color_ramp.elements[3].position = threshold * 1.5 if threshold * 1.5 <= 1.0 else 1.0
        color_ramp.color_ramp.elements[3].color = (0.95, 0.95, 1.0, 1.0) # Highlight

    # Links
    links.new(bsdf.outputs['BSDF'], shader_to_rgb.inputs['Shader'])
    links.new(shader_to_rgb.outputs['Color'], color_ramp.inputs['Fac'])
    links.new(color_ramp.outputs['Color'], output.inputs['Surface'])

    return mat

def create_pbr_material(mat_name):
    """Creates a basic PBR material using Principled BSDF."""
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    # The default node tree already has a Principled BSDF and Material Output
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
    mod.thickness = outline_config.get("width", 0.015) if isinstance(outline_config, dict) else 0.015
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
    for region_id, data in regions.items():
        indices = data.get("vertex_indices", []) if isinstance(data, dict) else []
        if indices:
            vg = obj.vertex_groups.new(name=region_id)
            vg.add(indices, 1.0, 'REPLACE')
            logging.info(f"Created vertex group {region_id} with {len(indices)} vertices")

    overrides = appearance.get("region_overrides", {}) if isinstance(appearance, dict) else {}
    if overrides:
        for region_id, style_override in overrides.items():
            if region_id in regions:
                logging.info(f"Applying style override for semantic region: {region_id}")

                mat_name = f"Mat_{obj.name}_{region_id}_Override"
                shading_conf = style_override.get("shading", {}) if isinstance(style_override, dict) else {}
                override_mat = create_toon_basic_material(mat_name, shading_conf)

                obj.data.materials.append(override_mat)
                mat_index = len(obj.data.materials) - 1

                # In headless, using bmesh is safer than bpy.ops for edit mode selections
                import bmesh
                bm = bmesh.new()
                bm.from_mesh(obj.data)

                deform_layer = bm.verts.layers.deform.verify()
                vg = obj.vertex_groups.get(region_id)

                if vg:
                    vg_index = vg.index
                    for face in bm.faces:
                        # Check if all vertices of the face belong to the vertex group
                        is_in_group = True
                        for vert in face.verts:
                            if vg_index not in vert[deform_layer]:
                                is_in_group = False
                                break

                        if is_in_group:
                            face.material_index = mat_index

                bm.to_mesh(obj.data)
                bm.free()

def extract_scene_report():
    report = {
        "environment": {
            "blender_version": ".".join(map(str, bpy.app.version)),
            "engine": 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types.SceneEEVEE, 'TAA_samples') else 'BLENDER_EEVEE',
        },
        "objects": [obj.name for obj in bpy.data.objects],
        "materials": [mat.name for mat in bpy.data.materials],
        "meshes": [mesh.name for mesh in bpy.data.meshes],
        "modifiers": {},
        "node_groups": [ng.name for ng in bpy.data.node_groups]
    }

    for obj in bpy.data.objects:
        if obj.modifiers:
            report["modifiers"][obj.name] = [mod.name for mod in obj.modifiers]

    return report

def main():
    try:
        args_str = os.environ.get("AOE_BLENDER_ARGS", "{}")
        args = json.loads(args_str)

        asset = args.get("asset", {})
        appearance = asset.get("appearance", {})
        family = appearance.get("family", "PBR")
        style = appearance.get("style", {})

        logging.info(f"AssetIR received: {asset.get('asset_id')}")
        logging.info(f"Appearance resolved: {family}")
        logging.info("Blender launched")

        # 1. Create Base Geometry (Monkey/Suzanne as test base if not specified)
        bpy.ops.mesh.primitive_monkey_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        obj = bpy.context.active_object
        obj.name = asset.get("asset_id", "AOE_Asset")
        logging.info(f"Scene created with base geometry: {obj.name}")

        # Apply Subdivision Surface for smoothness
        subsurf = obj.modifiers.new(name="Subsurf", type='SUBSURF')
        subsurf.levels = 2
        subsurf.render_levels = 2
        bpy.ops.object.modifier_apply(modifier="Subsurf")

        # 2. Shading setup
        shading_conf = style.get("shading", {}) if isinstance(style, dict) else {}
        if "NPR" in str(family) or family == "NPR" or "AppearanceFamily.NPR" in str(family):
            mat = create_toon_basic_material(f"Mat_{obj.name}_Toon", shading_conf)
            obj.data.materials.append(mat)
            logging.info(f"Material created (TOON_BASIC): {mat.name}")
        elif "PBR" in str(family) or family == "PBR" or "AppearanceFamily.PBR" in str(family):
            mat = create_pbr_material(f"Mat_{obj.name}_PBR")
            obj.data.materials.append(mat)
            logging.info(f"Material created (PBR): {mat.name}")

        # 3. Outline setup
        outline_conf = style.get("outline", {}) if isinstance(style, dict) else {}
        if outline_conf.get("enabled", False):
            outline_obj = apply_inverted_hull(obj, outline_conf)
            logging.info(f"Outline created: {outline_obj.name}")

        # 4. Semantic Regions setup
        semantic_regions = asset.get("semantic_regions", {})
        if semantic_regions:
            apply_semantic_materials(obj, appearance, semantic_regions)


        # Test Rigging Injection for Deformation Outline tests
        if "test_rig_pose" in asset.get("metadata", {}):
            pose_angle = asset.get("metadata")["test_rig_pose"]
            logging.info(f"Applying test armature deformation with angle {pose_angle}")

            # Select the original object (it should be the active one right now or outline_obj)
            bpy.context.view_layer.objects.active = obj

            # Create a simple armature
            bpy.ops.object.armature_add(location=(0, 0, 0))
            armature = bpy.context.active_object

            # Select mesh then armature and parent with automatic weights
            obj.select_set(True)
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')

            # Also parent the outline if it exists
            if outline_conf.get("enabled", False):
                # Deselect all
                bpy.ops.object.select_all(action='DESELECT')
                outline_obj.select_set(True)
                armature.select_set(True)
                bpy.context.view_layer.objects.active = armature
                # Important: Outline should ideally share the same vertex groups
                # Since we duplicated after subsurf but before armature in this script, it has no weights yet
                # For this test, we'll bind it too
                bpy.ops.object.parent_set(type='ARMATURE_AUTO')

                # VERY IMPORTANT: Solidify must happen AFTER Armature modifier for outline to inflate deformed mesh correctly
                # Reorder modifiers on outline
                # 1. Armature
                # 2. Outline_Solidify
                bpy.ops.object.select_all(action='DESELECT')
                outline_obj.select_set(True)
                bpy.context.view_layer.objects.active = outline_obj
                # The parent_set adds an Armature modifier at the end. We need to move it up.
                bpy.ops.object.modifier_move_to_index(modifier="Armature", index=0)


            # Pose it

            # Select armature to enter pose mode
            bpy.ops.object.select_all(action='DESELECT')
            armature.select_set(True)
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')

            pbone = armature.pose.bones[0]
            pbone.rotation_mode = 'XYZ'
            pbone.rotation_euler = (pose_angle, 0, 0)
            bpy.ops.object.mode_set(mode='OBJECT')

        # Extract Deep Report
        report = extract_scene_report()

        # Render if path is provided
        render_path = args.get("render_path")
        if render_path:
            logging.info("Render started")
            # Basic camera and light
            bpy.ops.object.camera_add(location=(0, -6, 1), rotation=(1.2, 0, 0))
            cam = bpy.context.active_object
            bpy.context.scene.camera = cam

            light_loc = asset.get("metadata", {}).get("test_light_loc", (0, 0, 5))
            bpy.ops.object.light_add(type='SUN', location=light_loc, rotation=(0.5, 0.5, 0))

            bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT' if hasattr(bpy.types.SceneEEVEE, 'TAA_samples') else 'BLENDER_EEVEE'
            bpy.context.scene.render.filepath = render_path
            bpy.ops.render.render(write_still=True)
            logging.info("Render completed")

        # Save .blend
        filepath = args.get("filepath")
        if filepath:
            bpy.ops.wm.save_as_mainfile(filepath=filepath)

        logging.info("Validation completed")

        result_data = {
            "status": "SUCCESS",
            "scene_report": report
        }

        print(f"AOE_RESULT:{json.dumps(result_data)}")
    except Exception as e:
        import traceback
        result_data = {
            "status": "FAILED",
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"AOE_RESULT:{json.dumps(result_data)}")

if __name__ == "__main__":
    main()
