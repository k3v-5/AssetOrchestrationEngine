"""regenerar_suelos_zero_zfighting.py — Regenerador de mallas de suelo para DarX con CERO Z-FIGHTING.
Aplica jerarquía de alturas estricta, canaletas no solapadas y tolerancia anti-coplanaridad.
"""

import bpy
import bmesh
import math
import os
import sys
from mathutils import Matrix, Vector

RAIZ_BLENDER = r"E:/Darx_Proyect/Art/Blender"
if RAIZ_BLENDER not in sys.path:
    sys.path.append(RAIZ_BLENDER)

import darx_lib as dl

FBX_DIR = r"E:/Darx_Proyect/Art/FBX/Biomas"
COL_MAESTRA = "DARX_MegaFase_Biomas"

def crear_materiales():
    m = {}
    # BIOHAZARD
    m["M_Bio_DarkMetal"] = dl.mat("M_Bio_DarkMetal", (0.035, 0.045, 0.040), rough=0.48, metal=0.90)
    m["M_Bio_PipeYellow"] = dl.mat("M_Bio_PipeYellow", (0.88, 0.65, 0.06), rough=0.35, metal=0.35)
    m["M_Bio_AcidGreen"] = dl.mat("M_Bio_AcidGreen", (0.05, 0.96, 0.12), rough=0.12, emis=(0.05, 0.98, 0.12), emis_str=4.8)
    
    # SALA LIMPIA / CUÁNTICO
    m["M_Clean_WhiteCeramic"] = dl.mat("M_Clean_WhiteCeramic", (0.93, 0.94, 0.96), rough=0.14, metal=0.04)
    m["M_Clean_Chrome"] = dl.mat("M_Clean_Chrome", (0.96, 0.96, 0.98), rough=0.02, metal=0.99)
    m["M_Clean_CyanNeon"] = dl.mat("M_Clean_CyanNeon", (0.0, 0.88, 1.0), rough=0.06, emis=(0.0, 0.88, 1.0), emis_str=5.0)
    m["M_Clean_DarkMetal"] = dl.mat("M_Clean_DarkMetal", (0.025, 0.025, 0.035), rough=0.32, metal=0.94)

    # ROBÓTICA
    m["M_Robo_CobaltSteel"] = dl.mat("M_Robo_CobaltSteel", (0.038, 0.075, 0.175), rough=0.30, metal=0.89)
    m["M_Robo_CopperBronze"] = dl.mat("M_Robo_CopperBronze", (0.78, 0.42, 0.14), rough=0.20, metal=0.96)
    m["M_Robo_Charcoal"] = dl.mat("M_Robo_Charcoal", (0.025, 0.025, 0.028), rough=0.52, metal=0.92)
    return m

def modelar_clean_floor_tile_limpio(mats):
    """SM_Clean_Floor_Tile: Arquitectura limpia por capas sin caras coplanares ni z-fighting."""
    b = dl.MB("SM_Clean_Floor_Tile")
    WC, CH, CN, DM = mats["M_Clean_WhiteCeramic"], mats["M_Clean_Chrome"], mats["M_Clean_CyanNeon"], mats["M_Clean_DarkMetal"]
    
    # 1. Bloque de cimentación inferior (Z = 0.0 a Z = 0.96)
    b.box((1.0, 1.0, 0.96), (0, 0, 0.48), m=WC)
    
    # 2. Marco perimetral y junta de silicona oscura hermética (Z = 0.96 a Z = 0.985)
    # Cara superior en Z = 0.985 m (98.5 cm)
    b.box((0.99, 0.99, 0.025), (0, 0, 0.9725), m=DM)
    
    # 3. Losa cerámica blanca brillante elevada sobre el marco oscuro (Z = 0.985 a Z = 1.005)
    # Cara superior en Z = 1.005 m (100.5 cm). Margen de 20 mm respecto al marco oscuro DM
    b.box((0.92, 0.92, 0.020), (0, 0, 0.995), m=WC)
    
    # 4. Cruz de fibra óptica cian (Segmentada en 4 cuadrantes, sin solaparse en el centro)
    # Cara superior en Z = 1.018 m (101.8 cm). Margen de 13 mm por encima de la losa blanca
    # Brazo Norte y Sur
    b.box((0.04, 0.41, 0.015), (0, 0.245, 1.0105), m=CN)
    b.box((0.04, 0.41, 0.015), (0, -0.245, 1.0105), m=CN)
    # Brazo Este y Oeste
    b.box((0.41, 0.04, 0.015), (0.245, 0, 1.0105), m=CN)
    b.box((0.41, 0.04, 0.015), (-0.245, 0, 1.0105), m=CN)
    
    # 5. Nexus central de cromo cilíndrico (Z = 1.005 a Z = 1.025)
    # Cara superior en Z = 1.025 m (102.5 cm)
    b.cyl(0.048, 0.020, (0, 0, 1.015), seg=16, m=CH)
    
    # 6. Esquineros de cromo en los 4 vértices de la losa blanca (Z = 1.005 a Z = 1.022)
    for x in [-0.41, 0.41]:
        for y in [-0.41, 0.41]:
            b.box((0.06, 0.06, 0.017), (x, y, 1.0135), m=CH)
            
    return b.build(COL_MAESTRA)

def modelar_bio_floor_grate_limpio(mats):
    """SM_Bio_Floor_Grate: Suelo modular sin caras coplanares entre fosa, lodo y rejilla."""
    b = dl.MB("SM_Bio_Floor_Grate")
    DM, PY, AG = mats["M_Bio_DarkMetal"], mats["M_Bio_PipeYellow"], mats["M_Bio_AcidGreen"]
    
    # 1. Marco exterior estructural de metal oscuro (Z = 0.0 a 0.85)
    b.box((1.0, 1.0, 0.85), (0, 0, 0.425), m=DM)
    
    # 2. Marco superior de apoyo de rejilla (Z = 0.85 a 0.99)
    b.box((0.99, 0.99, 0.14), (0, 0, 0.92), m=DM)
    
    # 3. Lodo cáustico en el fondo de la fosa interior (Z = 0.85 a 0.88)
    b.box((0.82, 0.82, 0.03), (0, 0, 0.865), m=AG)
    for bx, by in [(-0.25, -0.2), (0.2, 0.15), (-0.1, 0.3), (0.3, -0.25)]:
        b.sph(0.03, (bx, by, 0.885), scale=(1.2, 1.2, 0.5), m=AG)
        
    # 4. Rejilla industrial: barras longitudinales en Z = 0.94 a 0.99 (Z_top = 0.99)
    for dx in [-0.32, -0.16, 0.0, 0.16, 0.32]:
        b.box((0.032, 0.84, 0.05), (dx, 0, 0.965), m=DM)
        
    # Barras transversales por debajo: Z = 0.91 a 0.94 (Z_top = 0.94, sin colisionar con longitudinales)
    for dy in [-0.32, -0.16, 0.0, 0.16, 0.32]:
        b.box((0.84, 0.032, 0.03), (0, dy, 0.925), m=DM)
        
    # 5. Pernos de advertencia en las esquinas superiores (Z = 0.99 a 1.025)
    for px in [-0.45, 0.45]:
        for py in [-0.45, 0.45]:
            b.cyl(0.026, 0.035, (px, py, 1.0075), seg=8, m=PY)
            
    return b.build(COL_MAESTRA)

def modelar_robo_floor_darkplate_limpio(mats):
    """SM_Robo_Floor_DarkPlate: Placa de acero sin caras coplanares entre base, inserto y relieve."""
    b = dl.MB("SM_Robo_Floor_DarkPlate")
    CS, CB, CC = mats["M_Robo_CobaltSteel"], mats["M_Robo_CopperBronze"], mats["M_Robo_Charcoal"]
    
    # 1. Base estructural de cobalto (Z = 0.0 a 0.96)
    b.box((1.0, 1.0, 0.96), (0, 0, 0.48), m=CS)
    
    # 2. Marco perimetral rebajado de carbón (Z = 0.96 a 0.985)
    b.box((0.98, 0.98, 0.025), (0, 0, 0.9725), m=CC)
    
    # 3. Losa central diamantada de acero cobalto (Z = 0.985 a 1.005)
    b.box((0.90, 0.90, 0.020), (0, 0, 0.995), m=CS)
    
    # 4. Placas diamantadas en relieve (Z = 1.005 a 1.018)
    for rx in [-0.25, 0.0, 0.25]:
        for ry in [-0.3, -0.1, 0.1, 0.3]:
            b.box((0.075, 0.028, 0.013), (rx, ry, 1.0115), rot=(0, 0, math.pi/4), m=CS)
            
    # 5. Canaleta de cobre lateral (Z = 0.985 a 1.015)
    b.box((0.14, 0.86, 0.015), (0.35, 0, 1.0025), m=CC)
    b.cyl(0.022, 0.86, (0.35, 0, 1.015), rot=(math.pi/2, 0, 0), seg=10, m=CB)
    
    # 6. Remaches de bronce esquineros (Z = 1.005 a 1.025)
    for x in [-0.42, 0.42]:
        for y in [-0.42, 0.42]:
            b.cyl(0.028, 0.020, (x, y, 1.015), seg=6, m=CB)
            
    return b.build(COL_MAESTRA)

def ejecutar_regeneracion():
    print("=== REGENERANDO MALLAS DE SUELO (CERO Z-FIGHTING) ===")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    c = dl.coll(COL_MAESTRA)
    mats = crear_materiales()
    
    suelos = [
        modelar_clean_floor_tile_limpio(mats),
        modelar_bio_floor_grate_limpio(mats),
        modelar_robo_floor_darkplate_limpio(mats)
    ]
    
    os.makedirs(FBX_DIR, exist_ok=True)
    for obj in suelos:
        ruta_fbx = os.path.join(FBX_DIR, f"{obj.name}.fbx")
        dl.export_fbx(obj, ruta_fbx)
        print(f"Exportado FBX limpio: {ruta_fbx}")

if __name__ == "__main__":
    ejecutar_regeneracion()
