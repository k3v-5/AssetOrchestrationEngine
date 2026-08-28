import bpy
import bmesh
import math
from mathutils import Matrix, Vector, Quaternion
import os
import sys
import argparse

def parse_args():
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    parser = argparse.ArgumentParser()
    parser.add_argument("--blend-file", type=str, default="")
    parser.add_argument("--preview-output", type=str, default="")
    return parser.parse_args(argv)

def clean_collection(col_name="AOE_Player_DarkFluid"):
    if col_name in bpy.data.collections:
        col = bpy.data.collections[col_name]
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        return col
    col = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(col)
    return col

def create_liquid_black_purple_shader(name="M_DarX_DarkFluid_BlackPurple"):
    if name in bpy.data.materials:
        mat = bpy.data.materials[name]
        mat.node_tree.nodes.clear()
    else:
        mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    nodes = nt.nodes
    links = nt.links

    # 1. Output & Principled BSDF
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (1000, 0)

    bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
    bsdf.location = (650, 0)
    links.new(bsdf.outputs["BSDF"], output_node.inputs["Surface"])

    # High Gloss Mirror Liquid Obsidian Ferrofluid
    bsdf.inputs["Metallic"].default_value = 0.92
    bsdf.inputs["Roughness"].default_value = 0.03
    if "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = 1.65
    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = 1.0
        bsdf.inputs["Coat Roughness"].default_value = 0.01
    elif "Clearcoat" in bsdf.inputs:
        bsdf.inputs["Clearcoat"].default_value = 1.0
        bsdf.inputs["Clearcoat Roughness"].default_value = 0.01

    # 2. Coordinates & Mapping
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_coord.location = (-900, 0)

    mapping = nodes.new(type="ShaderNodeMapping")
    mapping.location = (-700, 0)
    mapping.inputs["Scale"].default_value = (1.4, 1.4, 1.1)
    links.new(tex_coord.outputs["Object"], mapping.inputs["Vector"])

    # 3. Organic Fluid Currents (Low frequency, sleek liquid streams)
    noise1 = nodes.new(type="ShaderNodeTexNoise")
    noise1.location = (-500, 150)
    noise1.inputs["Scale"].default_value = 1.6
    noise1.inputs["Detail"].default_value = 4.0
    noise1.inputs["Roughness"].default_value = 0.45
    noise1.inputs["Distortion"].default_value = 4.5
    links.new(mapping.outputs["Vector"], noise1.inputs["Vector"])

    noise2 = nodes.new(type="ShaderNodeTexNoise")
    noise2.location = (-500, -150)
    noise2.inputs["Scale"].default_value = 3.2
    noise2.inputs["Detail"].default_value = 5.0
    noise2.inputs["Roughness"].default_value = 0.50
    noise2.inputs["Distortion"].default_value = 2.5
    links.new(mapping.outputs["Vector"], noise2.inputs["Vector"])

    mix_noise = nodes.new(type="ShaderNodeMix")
    mix_noise.data_type = 'FLOAT'
    mix_noise.location = (-300, 0)
    mix_noise.inputs["Factor"].default_value = 0.35
    links.new(noise1.outputs["Fac"], mix_noise.inputs[2])
    links.new(noise2.outputs["Fac"], mix_noise.inputs[3])

    # 4. ColorRamp: 75% Deep Obsidian Black + 25% Vibrant Neon Violet/Purple Energy Streams
    color_ramp = nodes.new(type="ShaderNodeValToRGB")
    color_ramp.location = (-50, 150)
    elements = color_ramp.color_ramp.elements
    elements.remove(elements[1])

    # Pos 0.50: Pure Glossy Liquid Obsidian Black Base (Dominant 75%)
    elements[0].position = 0.50
    elements[0].color = (0.003, 0.003, 0.005, 1.0)

    # Pos 0.58: Deep Midnight Violet Undertone
    e1 = elements.new(0.58)
    e1.color = (0.18, 0.01, 0.45, 1.0)

    # Pos 0.68: Electric Neon Violet / Purple Current
    e2 = elements.new(0.68)
    e2.color = (0.65, 0.02, 0.98, 1.0)

    # Pos 0.80: Intense Neon Purple / Magenta Detail
    e3 = elements.new(0.80)
    e3.color = (0.90, 0.02, 1.0, 1.0)

    # Pos 0.92: Brilliant White-Hot Violet Plasma Core
    e4 = elements.new(0.92)
    e4.color = (1.0, 0.65, 1.0, 1.0)

    links.new(mix_noise.outputs[0], color_ramp.inputs["Fac"])
    links.new(color_ramp.outputs["Color"], bsdf.inputs["Base Color"])

    # 5. Layer Weight Fresnel Rim (Rebotes con luz morado en silueta)
    layer_weight = nodes.new(type="ShaderNodeLayerWeight")
    layer_weight.location = (-50, 400)
    layer_weight.inputs["Blend"].default_value = 0.25

    # 6. Emission Mask & Strength (Purple Energy Details + Edge Sheen)
    emit_ramp = nodes.new(type="ShaderNodeValToRGB")
    emit_ramp.location = (-50, -150)
    emit_elements = emit_ramp.color_ramp.elements
    emit_elements[0].position = 0.56
    emit_elements[0].color = (0, 0, 0, 1)
    emit_elements[1].position = 0.84
    emit_elements[1].color = (1, 1, 1, 1)
    links.new(mix_noise.outputs[0], emit_ramp.inputs["Fac"])

    # Combine vein emission + grazing rim emission
    mix_emit = nodes.new(type="ShaderNodeMix")
    mix_emit.data_type = 'FLOAT'
    mix_emit.location = (180, 200)
    mix_emit.inputs["Factor"].default_value = 0.45
    links.new(emit_ramp.outputs["Color"], mix_emit.inputs[2])
    links.new(layer_weight.outputs["Facing"], mix_emit.inputs[3])

    math_strength = nodes.new(type="ShaderNodeMath")
    math_strength.location = (350, -100)
    math_strength.operation = 'MULTIPLY'
    math_strength.inputs[1].default_value = 28.0
    links.new(mix_emit.outputs[0], math_strength.inputs[0])

    if "Emission Color" in bsdf.inputs:
        links.new(color_ramp.outputs["Color"], bsdf.inputs["Emission Color"])
        links.new(math_strength.outputs["Value"], bsdf.inputs["Emission Strength"])
    elif "Emission" in bsdf.inputs:
        links.new(color_ramp.outputs["Color"], bsdf.inputs["Emission"])

    # 7. Fluid Ripple Bump / Normal
    bump = nodes.new(type="ShaderNodeBump")
    bump.location = (350, -320)
    bump.inputs["Strength"].default_value = 0.05
    bump.inputs["Distance"].default_value = 0.02
    links.new(mix_noise.outputs[0], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    return mat

def add_capsule_segment(bm, p1, p2, r1, r2):
    v1 = Vector(p1)
    v2 = Vector(p2)
    dir_vec = v2 - v1
    dist = dir_vec.length
    if dist < 0.001:
        return
    
    mid = (v1 + v2) * 0.5
    up = Vector((0, 0, 1))
    rot = up.rotation_difference(dir_vec.normalized())
    
    mat_rot = rot.to_matrix().to_4x4()
    mat_trans = Matrix.Translation(mid)
    
    mat_cyl = mat_trans @ mat_rot @ Matrix.Diagonal(((r1 + r2)*0.5, (r1 + r2)*0.5, dist, 1.0))
    bmesh.ops.create_cube(bm, size=1.0, matrix=mat_cyl)
    
    mat_s1 = Matrix.Translation(v1) @ Matrix.Diagonal((r1, r1, r1, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_s1)
    mat_s2 = Matrix.Translation(v2) @ Matrix.Diagonal((r2, r2, r2, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_s2)

def build_sculpted_humanoid_runner(col):
    mesh = bpy.data.meshes.new("SK_Player_DarkFluid_Body_Mesh")
    obj = bpy.data.objects.new("SK_Player_DarkFluid_Body", mesh)
    col.objects.link(obj)

    bm = bmesh.new()

    # 1. Torso Spine Core (Athletic forward sprint posture)
    pelvis = (0.0, 0.0, 0.95)
    lower_abs = (0.0, 0.10, 1.10)
    upper_abs = (0.0, 0.20, 1.25)
    chest_core = (0.0, 0.32, 1.40)
    neck_base = (0.0, 0.42, 1.56)
    head_center = (0.0, 0.54, 1.70)

    add_capsule_segment(bm, pelvis, lower_abs, 0.17, 0.15)
    add_capsule_segment(bm, lower_abs, upper_abs, 0.15, 0.17)
    add_capsule_segment(bm, upper_abs, chest_core, 0.17, 0.23)
    add_capsule_segment(bm, chest_core, neck_base, 0.23, 0.10)
    add_capsule_segment(bm, neck_base, head_center, 0.10, 0.13)

    # 2. Pectorals & Abs
    mat_pec_r = Matrix.Translation((0.11, 0.36, 1.38)) @ Matrix.Diagonal((0.15, 0.13, 0.15, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_pec_r)
    mat_pec_l = Matrix.Translation((-0.11, 0.36, 1.38)) @ Matrix.Diagonal((0.15, 0.13, 0.15, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_pec_l)

    for z_off, y_off, w in [(1.26, 0.24, 0.065), (1.18, 0.16, 0.07), (1.10, 0.10, 0.075)]:
        mat_ab_r = Matrix.Translation((0.06, y_off, z_off)) @ Matrix.Diagonal((w, 0.055, 0.055, 1.0))
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_ab_r)
        mat_ab_l = Matrix.Translation((-0.06, y_off, z_off)) @ Matrix.Diagonal((w, 0.055, 0.055, 1.0))
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_ab_l)

    # Clavicles
    add_capsule_segment(bm, (0.0, 0.38, 1.52), (0.24, 0.30, 1.46), 0.06, 0.055)
    add_capsule_segment(bm, (0.0, 0.38, 1.52), (-0.24, 0.30, 1.46), 0.06, 0.055)

    # 3. RIGHT ARM (Forward Sprint Lead Arm - Outstretched Palm)
    sh_r = (0.25, 0.28, 1.42)
    elbow_r = (0.38, 0.58, 1.36)
    wrist_r = (0.32, 0.84, 1.48)
    palm_r = (0.26, 1.00, 1.56)

    mat_delt_r = Matrix.Translation(sh_r) @ Matrix.Diagonal((0.13, 0.12, 0.13, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_delt_r)

    add_capsule_segment(bm, sh_r, elbow_r, 0.10, 0.085)
    add_capsule_segment(bm, elbow_r, wrist_r, 0.085, 0.065)
    add_capsule_segment(bm, wrist_r, palm_r, 0.065, 0.045)

    for f_idx, (fx, fy, fz) in enumerate([
        (0.30, 1.12, 1.64),
        (0.26, 1.14, 1.62),
        (0.22, 1.12, 1.58),
        (0.18, 1.08, 1.54),
        (0.34, 1.02, 1.52)
    ]):
        add_capsule_segment(bm, palm_r, (fx, fy, fz), 0.020, 0.008)

    # 4. LEFT ARM (Pumped Backward in Sprint Stride)
    sh_l = (-0.25, 0.24, 1.42)
    elbow_l = (-0.38, -0.06, 1.28)
    wrist_l = (-0.36, -0.28, 1.12)
    palm_l = (-0.32, -0.42, 1.00)

    mat_delt_l = Matrix.Translation(sh_l) @ Matrix.Diagonal((0.13, 0.12, 0.13, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_delt_l)

    add_capsule_segment(bm, sh_l, elbow_l, 0.10, 0.085)
    add_capsule_segment(bm, elbow_l, wrist_l, 0.085, 0.065)
    add_capsule_segment(bm, wrist_l, palm_l, 0.065, 0.045)

    for f_idx, (fx, fy, fz) in enumerate([
        (-0.36, -0.54, 0.94),
        (-0.32, -0.56, 0.92),
        (-0.28, -0.54, 0.90),
        (-0.24, -0.50, 0.88),
        (-0.38, -0.46, 0.98)
    ]):
        add_capsule_segment(bm, palm_l, (fx, fy, fz), 0.020, 0.008)

    # 5. RIGHT LEG (High Knee Driving Forward)
    hip_r = (0.14, 0.06, 0.92)
    knee_r = (0.18, 0.44, 0.86)
    ankle_r = (0.18, 0.56, 0.40)
    foot_r = (0.18, 0.64, 0.20)

    add_capsule_segment(bm, pelvis, hip_r, 0.15, 0.13)
    add_capsule_segment(bm, hip_r, knee_r, 0.13, 0.10)
    mat_quad_r = Matrix.Translation((0.18, 0.28, 0.92)) @ Matrix.Diagonal((0.13, 0.14, 0.20, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_quad_r)

    mat_knee_r = Matrix.Translation(knee_r) @ Matrix.Diagonal((0.09, 0.10, 0.09, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_knee_r)

    add_capsule_segment(bm, knee_r, ankle_r, 0.10, 0.075)
    mat_calf_r = Matrix.Translation((0.18, 0.48, 0.52)) @ Matrix.Diagonal((0.11, 0.12, 0.16, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_calf_r)

    add_capsule_segment(bm, ankle_r, foot_r, 0.075, 0.045)

    # 6. LEFT LEG (Extended Back Off Ground)
    hip_l = (-0.14, -0.04, 0.92)
    knee_l = (-0.18, -0.34, 0.68)
    ankle_l = (-0.18, -0.72, 0.32)
    foot_l = (-0.18, -0.90, 0.14)

    add_capsule_segment(bm, pelvis, hip_l, 0.15, 0.13)
    add_capsule_segment(bm, hip_l, knee_l, 0.13, 0.10)
    mat_ham_l = Matrix.Translation((-0.18, -0.18, 0.80)) @ Matrix.Diagonal((0.13, 0.14, 0.20, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_ham_l)

    add_capsule_segment(bm, knee_l, ankle_l, 0.10, 0.075)
    mat_calf_l = Matrix.Translation((-0.18, -0.54, 0.50)) @ Matrix.Diagonal((0.11, 0.12, 0.16, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_calf_l)

    add_capsule_segment(bm, ankle_l, foot_l, 0.075, 0.045)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    obj.data.remesh_voxel_size = 0.016
    bpy.ops.object.voxel_remesh()

    sm = obj.modifiers.new("Smooth", type='SMOOTH')
    sm.factor = 0.5
    sm.iterations = 3

    sub = obj.modifiers.new("Subsurf", type='SUBSURF')
    sub.levels = 1
    sub.render_levels = 1

    for poly in obj.data.polygons:
        poly.use_smooth = True

    return obj

def build_faceted_crystal_head(col):
    mesh = bpy.data.meshes.new("SK_Player_FacetedHead_Mesh")
    obj = bpy.data.objects.new("SK_Player_FacetedHead", mesh)
    col.objects.link(obj)

    bm = bmesh.new()
    # Geometric low-poly faceted head crystal mask (flat shaded!)
    mat_head = Matrix.Translation((0.0, 0.54, 1.70)) @ Matrix.Diagonal((0.24, 0.28, 0.32, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.5, matrix=mat_head)

    # Rear fluid crest
    mat_crest = Matrix.Translation((0.0, 0.38, 1.80)) @ Matrix.Rotation(math.radians(-35), 4, 'X') @ Matrix.Diagonal((0.14, 0.26, 0.14, 1.0))
    bmesh.ops.create_icosphere(bm, subdivisions=1, radius=0.5, matrix=mat_crest)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    for poly in obj.data.polygons:
        poly.use_smooth = False

    return obj

def build_dense_fluid_splashes(col):
    mesh = bpy.data.meshes.new("SK_Player_FluidSplashes_Mesh")
    obj = bpy.data.objects.new("SK_Player_FluidSplashes", mesh)
    col.objects.link(obj)

    bm = bmesh.new()

    splashes = [
        # Back & spine trailing fluid spikes
        ((-0.06, 0.12, 1.44), (-0.12, -0.12, 1.36), 0.028, 0.007),
        ((0.06, 0.12, 1.44), (0.12, -0.12, 1.36), 0.028, 0.007),
        ((0.00, 0.04, 1.28), (0.00, -0.20, 1.18), 0.032, 0.007),
        # Right Lead Arm / Hand splash tendrils
        ((0.28, 0.92, 1.50), (0.36, 1.10, 1.56), 0.022, 0.005),
        ((0.24, 1.00, 1.56), (0.22, 1.16, 1.64), 0.018, 0.004),
        # Left Drawn Arm drops
        ((-0.38, -0.06, 1.28), (-0.46, -0.18, 1.22), 0.024, 0.007),
        ((-0.32, -0.42, 1.00), (-0.38, -0.58, 0.92), 0.020, 0.005),
        # Right Back Leg / Heel trailing stream
        ((0.18, -0.72, 0.32), (0.22, -0.92, 0.24), 0.026, 0.007),
        ((0.18, -0.90, 0.14), (0.22, -1.10, 0.08), 0.024, 0.005),
        # Left Knee splash
        ((-0.18, 0.44, 0.86), (-0.24, 0.58, 0.92), 0.024, 0.005)
    ]

    for p1, p2, r1, r2 in splashes:
        add_capsule_segment(bm, p1, p2, r1, r2)

    droplets = [
        (-0.16, -0.18, 1.34, 0.018),
        (0.16, -0.18, 1.34, 0.018),
        (0.00, -0.28, 1.14, 0.022),
        (0.40, 1.18, 1.62, 0.015),
        (0.20, 1.22, 1.68, 0.013),
        (-0.50, -0.24, 1.18, 0.016),
        (-0.42, -0.62, 0.88, 0.015),
        (-0.26, 0.64, 0.96, 0.018),
        (0.24, -0.98, 0.20, 0.018),
        (0.22, -1.18, 0.06, 0.015),
        (0.12, -0.32, 1.42, 0.011),
        (-0.12, -0.32, 1.42, 0.011),
        (0.46, -0.12, 1.32, 0.013),
        (-0.40, 0.50, 1.47, 0.013),
        (0.24, 0.74, 0.50, 0.013),
        (-0.20, -0.82, 0.40, 0.013)
    ]
    for x, y, z, r in droplets:
        mat_drop = Matrix.Translation((x, y, z)) @ Matrix.Diagonal((r, r, r * 1.5, 1.0))
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0, matrix=mat_drop)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    for poly in obj.data.polygons:
        poly.use_smooth = True

    return obj

def build_scifi_studio_environment(col):
    mesh = bpy.data.meshes.new("ENV_SciFi_Studio_Lab_Mesh")
    obj = bpy.data.objects.new("ENV_SciFi_Studio_Lab", mesh)
    col.objects.link(obj)

    bm = bmesh.new()
    # Floor Panel Grid (White glossy tiles)
    mat_floor = Matrix.Translation((0, 0, -0.01)) @ Matrix.Diagonal((16.0, 16.0, 0.02, 1.0))
    bmesh.ops.create_cube(bm, size=1.0, matrix=mat_floor)

    # Floor Light Lines
    for y_pos in [-3.0, -1.5, 0.0, 1.5, 3.0, 4.5]:
        mat_strip = Matrix.Translation((0, y_pos, 0.01)) @ Matrix.Diagonal((14.0, 0.12, 0.01, 1.0))
        bmesh.ops.create_cube(bm, size=1.0, matrix=mat_strip)

    # Background White Architecture Pillars
    for x_pos in [-4.5, 4.5]:
        for y_pos in [-3.0, 0.5, 4.0]:
            mat_pillar = Matrix.Translation((x_pos, y_pos, 2.5)) @ Matrix.Diagonal((0.6, 0.6, 5.0, 1.0))
            bmesh.ops.create_cube(bm, size=1.0, matrix=mat_pillar)

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    mat_lab = bpy.data.materials.get("M_DarX_LabWhiteCeramic")
    if not mat_lab:
        mat_lab = bpy.data.materials.new("M_DarX_LabWhiteCeramic")
        mat_lab.use_nodes = True
        bsdf = mat_lab.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = (0.86, 0.89, 0.93, 1.0)
            bsdf.inputs["Metallic"].default_value = 0.10
            bsdf.inputs["Roughness"].default_value = 0.20
    obj.data.materials.clear()
    obj.data.materials.append(mat_lab)
    return obj

def setup_lights():
    scene = bpy.context.scene
    # 1. Main Studio Key Light (Front Right)
    key_name = "AOE_Player_Light_Key"
    if key_name in bpy.data.objects:
        key_obj = bpy.data.objects[key_name]
    else:
        k_data = bpy.data.lights.new(key_name, type='SUN')
        key_obj = bpy.data.objects.new(key_name, k_data)
        scene.collection.objects.link(key_obj)
    key_obj.data.energy = 2.8
    key_obj.data.color = (1.0, 0.98, 0.96)
    key_obj.location = (4.0, 4.0, 4.2)
    key_obj.rotation_euler = (math.radians(45), math.radians(-15), math.radians(-45))

    # 2. Strong Violet/Purple Rim Light (For Rich Purple Specular Bounces)
    rim_name = "AOE_Player_Light_Rim"
    if rim_name in bpy.data.objects:
        rim_obj = bpy.data.objects[rim_name]
    else:
        r_data = bpy.data.lights.new(rim_name, type='SUN')
        rim_obj = bpy.data.objects.new(rim_name, r_data)
        scene.collection.objects.link(rim_obj)
    rim_obj.data.energy = 5.5
    rim_obj.data.color = (0.85, 0.02, 1.0) # Vivid neon purple rim light!
    rim_obj.location = (-4.0, -4.0, 2.8)
    rim_obj.rotation_euler = (math.radians(-50), math.radians(20), math.radians(135))

    # 3. Soft Fill Light (Neutral Cool)
    fill_name = "AOE_Player_Light_Fill"
    if fill_name in bpy.data.objects:
        fill_obj = bpy.data.objects[fill_name]
    else:
        f_data = bpy.data.lights.new(fill_name, type='SUN')
        fill_obj = bpy.data.objects.new(fill_name, f_data)
        scene.collection.objects.link(fill_obj)
    fill_obj.data.energy = 1.4
    fill_obj.data.color = (0.85, 0.88, 0.95)
    fill_obj.location = (0.0, 2.5, 0.4)

def render_camera_view(cam_pos, target_pos, lens, output_file, res=(960, 540)):
    scene = bpy.context.scene
    scene.render.resolution_x = res[0]
    scene.render.resolution_y = res[1]

    cam_name = "AOE_Player_Cam_Dyn"
    if cam_name in bpy.data.objects:
        cam_obj = bpy.data.objects[cam_name]
    else:
        cam_data = bpy.data.cameras.new(cam_name)
        cam_obj = bpy.data.objects.new(cam_name, cam_data)
        scene.collection.objects.link(cam_obj)

    cam_obj.location = cam_pos
    cam_obj.data.lens = lens
    cam_obj.constraints.clear()

    empty_name = "AOE_Player_Cam_Dyn_Target"
    if empty_name in bpy.data.objects:
        target_empty = bpy.data.objects[empty_name]
    else:
        target_empty = bpy.data.objects.new(empty_name, None)
        scene.collection.objects.link(target_empty)
    target_empty.location = target_pos

    tt = cam_obj.constraints.new(type='TRACK_TO')
    tt.target = target_empty
    tt.track_axis = 'TRACK_NEGATIVE_Z'
    tt.up_axis = 'UP_Y'
    scene.camera = cam_obj

    scene.render.filepath = output_file
    bpy.ops.render.render(write_still=True)

def render_all_views(output_base_dir):
    os.makedirs(output_base_dir, exist_ok=True)
    scene = bpy.context.scene
    if scene.world:
        scene.world.use_nodes = True
        bg = scene.world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs["Color"].default_value = (0.86, 0.89, 0.93, 1.0)
            bg.inputs["Strength"].default_value = 0.8

    setup_lights()

    # 1. Front-3/4 Action (Matching reference sprint composition)
    v1_file = os.path.join(output_base_dir, "view_action_34.png")
    render_camera_view((2.7, 2.7, 1.45), (0.0, 0.12, 1.00), 40.0, v1_file, res=(1920, 1080))
    print(f"RENDERED: {v1_file}")

    # 2. Front View (Chest, Pectorals, 6-pack abs, Head visor)
    v2_file = os.path.join(output_base_dir, "view_front.png")
    render_camera_view((0.0, 3.6, 1.25), (0.0, 0.12, 1.05), 45.0, v2_file, res=(960, 540))
    print(f"RENDERED: {v2_file}")

    # 3. Back View (Spine, Glutes, Back fluid tendrils)
    v3_file = os.path.join(output_base_dir, "view_back.png")
    render_camera_view((0.0, -3.6, 1.25), (0.0, 0.0, 1.05), 45.0, v3_file, res=(960, 540))
    print(f"RENDERED: {v3_file}")

    # 4. First-Person View (Forearm, 5-finger palm with fluid droplets)
    v4_file = os.path.join(output_base_dir, "view_fps.png")
    render_camera_view((0.10, 0.65, 1.62), (0.26, 1.00, 1.56), 28.0, v4_file, res=(960, 540))
    print(f"RENDERED: {v4_file}")

def main():
    args = parse_args()
    col = clean_collection("AOE_Player_DarkFluid")

    # 1. Build athletic humanoid runner body & faceted crystal head
    body = build_sculpted_humanoid_runner(col)
    head = build_faceted_crystal_head(col)
    droplets = build_dense_fluid_splashes(col)
    env = build_scifi_studio_environment(col)

    # 2. Create and apply the predominantly black obsidian shader with purple energy & light bounces
    black_purple_mat = create_liquid_black_purple_shader("M_DarX_DarkFluid_BlackPurple")

    body.data.materials.clear()
    body.data.materials.append(black_purple_mat)

    head.data.materials.clear()
    head.data.materials.append(black_purple_mat)

    droplets.data.materials.clear()
    droplets.data.materials.append(black_purple_mat)

    for obj in bpy.data.objects:
        if obj.name not in ["SK_Player_DarkFluid_Body", "SK_Player_FacetedHead", "SK_Player_FluidSplashes", "ENV_SciFi_Studio_Lab"] and not obj.name.startswith("AOE_Player_"):
            obj.hide_render = True
        else:
            obj.hide_render = False

    if args.preview_output:
        out_dir = os.path.dirname(os.path.abspath(args.preview_output))
        render_all_views(out_dir)

    if args.blend_file:
        bpy.ops.wm.save_as_mainfile(filepath=args.blend_file)
        print(f"FILE_SAVED: {args.blend_file}")

if __name__ == "__main__":
    main()
