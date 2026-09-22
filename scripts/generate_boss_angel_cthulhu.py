"""generate_boss_angel_cthulhu.py — Modelado 3D, Armadura, Renders 4 Vistas y Exportación FBX de Azra'Koth.

Jefe: Azra'Koth, El Serafín Primordial (Ángel-Cthulhu con extremidades articuladas en vez de tentáculos).
Dimensiones aproximadas: Altura 4.20 m, Envergadura de alas 5.50 m.
Pivote en el suelo (Z=0), Frente = -Y, Arriba = +Z (Regla 13).

DISEÑO: HÍBRIDO ÁNGEL SERAFÍN / CTHULHU BIOMECÁNICO
---------------------------------------------------
- Cabeza abovedada cefalópoda con cresta ósea y 8 ojos estigmáticos laterales.
- 4 extremidades prensiles frontales articuladas (3 falanges con espinas y quelíceros) en vez de tentáculos blandos.
- Fauce radial de triple mandíbula.
- Aureola celestial de espinas óseas flotante sobre la cabeza.
- Torso acorazado con corazón de savia bioluminiscente expuesto en el esternón.
- 6 Alas serafín biomecánicas (3 pares articulados: alas superiores de envergadura masiva, alas medias acorazadas y alas inferiores estabilizadoras).
- Brazos principales con garras de 4 dedos y brazos secundarios pectorales canalizadores.
- Tren inferior levitante con 2 patas rapaces digitígradas con espolones.

Cumple con:
- Regla 3: Diseño 100% único, sin reciclar maniquíes ni mallas existentes.
- Reglas 4 y 5: Render de 4 vistas (Frontal, Trasera, Acción/Ataque, Vista FPS) antes de importar a UE5.
- Regla 11: 5 fases de modelado 3D.
- Regla 12: Cinemática con sockets canónicos y congruencia de Rest Pose.
- Regla 13: Eje canónico -Y en Blender -> +X en Unreal Engine.
"""

import bpy
import bmesh
import math
import os
import sys
from mathutils import Matrix, Vector, Euler

RAIZ_BLENDER = r"E:/Darx_Proyect/Art/Blender"
if RAIZ_BLENDER not in sys.path:
    sys.path.append(RAIZ_BLENDER)

import darx_lib as dl

COL_BOSS = "DARX_Boss_AngelCthulhu"
ARTIFACTS_DIR = r"C:\Users\sasuk\.gemini\antigravity\brain\695523dc-0f49-434f-b134-d3298443b0f2"
FBX_DIR = r"E:/Darx_Proyect/Art/FBX"

def crear_materiales_boss():
    m = {}
    # Quitina oscura bioluminiscente
    m["M_Bio_DarkChitin"] = dl.mat("M_Bio_DarkChitin", (0.022, 0.028, 0.025), rough=0.38, metal=0.85)
    # Hueso marfil / serafín
    m["M_Angel_Bone"] = dl.mat("M_Angel_Bone", (0.85, 0.82, 0.76), rough=0.25, metal=0.15)
    # Oro celestial acentuado
    m["M_Angel_Gold"] = dl.mat("M_Angel_Gold", (0.92, 0.72, 0.18), rough=0.18, metal=0.95)
    # Savia ácida fluorescente (520 nm)
    m["M_Bio_AcidGreen"] = dl.mat("M_Bio_AcidGreen", (0.05, 0.98, 0.12), rough=0.08,
                                  emis=(0.05, 0.98, 0.12), emis_str=5.5)
    # Ojos estigmáticos carmesí
    m["M_Bio_EyeCrimson"] = dl.mat("M_Bio_EyeCrimson", (1.0, 0.03, 0.02), rough=0.04,
                                   emis=(1.0, 0.03, 0.02), emis_str=6.0)
    # Plumas de energía etérea
    m["M_Angel_EnergyWing"] = dl.mat("M_Angel_EnergyWing", (0.15, 0.92, 0.65), rough=0.05, metal=0.05,
                                     emis=(0.10, 0.88, 0.55), emis_str=4.2)
    return m

def build_boss_armature():
    """Crea la armadura ósea canónica para Azra'Koth."""
    arm_data = bpy.data.armatures.new("Armature_Boss_AngelCthulhu")
    arm_obj = bpy.data.objects.new("Armature_SK_Boss_AngelCthulhu", arm_data)
    bpy.context.scene.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    bpy.ops.object.mode_set(mode='EDIT')
    eb = arm_data.edit_bones

    # 1. Root
    b_root = eb.new("root")
    b_root.head = (0, 0, 0)
    b_root.tail = (0, 0, 0.30)

    # 2. Pelvis
    b_pelvis = eb.new("pelvis")
    b_pelvis.head = (0, 0, 1.40)
    b_pelvis.tail = (0, 0, 1.70)
    b_pelvis.parent = b_root

    # 3. Columna vertebral
    b_spine1 = eb.new("spine_01")
    b_spine1.head = (0, 0, 1.70)
    b_spine1.tail = (0, -0.05, 2.20)
    b_spine1.parent = b_pelvis

    b_spine2 = eb.new("spine_02")
    b_spine2.head = (0, -0.05, 2.20)
    b_spine2.tail = (0, -0.10, 2.80)
    b_spine2.parent = b_spine1

    # 4. Cuello y Cabeza Cefalópoda
    b_neck = eb.new("neck")
    b_neck.head = (0, -0.10, 2.80)
    b_neck.tail = (0, -0.15, 3.15)
    b_neck.parent = b_spine2

    b_head = eb.new("head")
    b_head.head = (0, -0.15, 3.15)
    b_head.tail = (0, -0.30, 3.65)
    b_head.parent = b_neck

    # 5. Aureola Celestial Flotante
    b_halo = eb.new("halo_root")
    b_halo.head = (0, -0.15, 3.85)
    b_halo.tail = (0, -0.15, 4.20)
    b_halo.parent = b_head

    # 6. 4 Extremidades Mandibulares Articuladas (Garras Faciales en vez de tentáculos)
    pos_queliceros = [
        ("mandible_l1", -0.22, -0.35, 3.15),
        ("mandible_l2", -0.12, -0.42, 2.95),
        ("mandible_r1",  0.22, -0.35, 3.15),
        ("mandible_r2",  0.12, -0.42, 2.95),
    ]
    for b_nom, qx, qy, qz in pos_queliceros:
        # Base de la extremidad
        b_qbase = eb.new(f"{b_nom}_base")
        b_qbase.head = (qx * 0.6, qy * 0.7, qz)
        b_qbase.tail = (qx, qy, qz - 0.20)
        b_qbase.parent = b_head

        # Falange intermedia
        b_qmid = eb.new(f"{b_nom}_mid")
        b_qmid.head = (qx, qy, qz - 0.20)
        b_qmid.tail = (qx * 1.15, qy - 0.25, qz - 0.45)
        b_qmid.parent = b_qbase

        # Garra/punta
        b_qtip = eb.new(f"{b_nom}_claw")
        b_qtip.head = (qx * 1.15, qy - 0.25, qz - 0.45)
        b_qtip.tail = (qx * 0.8, qy - 0.40, qz - 0.65)
        b_qtip.parent = b_qmid

    # 7. 6 Alas Serafín Biomecánicas (3 pares en la espalda)
    for lado, sx in [("l", -1.0), ("r", 1.0)]:
        # Alas superiores (Envergadura colosal)
        b_w_up1 = eb.new(f"wing_{lado}_upper_01")
        b_w_up1.head = (0.20 * sx, 0.15, 2.70)
        b_w_up1.tail = (1.20 * sx, 0.40, 3.60)
        b_w_up1.parent = b_spine2

        b_w_up2 = eb.new(f"wing_{lado}_upper_02")
        b_w_up2.head = (1.20 * sx, 0.40, 3.60)
        b_w_up2.tail = (2.40 * sx, 0.60, 4.30)
        b_w_up2.parent = b_w_up1

        # Alas medias (Acorazadas de cobertura)
        b_w_mid1 = eb.new(f"wing_{lado}_mid_01")
        b_w_mid1.head = (0.22 * sx, 0.12, 2.35)
        b_w_mid1.tail = (1.30 * sx, 0.35, 2.65)
        b_w_mid1.parent = b_spine2

        b_w_mid2 = eb.new(f"wing_{lado}_mid_02")
        b_w_mid2.head = (1.30 * sx, 0.35, 2.65)
        b_w_mid2.tail = (2.10 * sx, 0.50, 2.80)
        b_w_mid2.parent = b_w_mid1

        # Alas inferiores (Estabilizadoras caudales)
        b_w_low1 = eb.new(f"wing_{lado}_low_01")
        b_w_low1.head = (0.18 * sx, 0.08, 1.85)
        b_w_low1.tail = (1.00 * sx, 0.25, 1.45)
        b_w_low1.parent = b_spine1

        b_w_low2 = eb.new(f"wing_{lado}_low_02")
        b_w_low2.head = (1.00 * sx, 0.25, 1.45)
        b_w_low2.tail = (1.70 * sx, 0.35, 0.95)
        b_w_low2.parent = b_w_low1

        # 8. Brazos Primarios
        b_arm_up = eb.new(f"arm_{lado}_upper")
        b_arm_up.head = (0.45 * sx, -0.10, 2.65)
        b_arm_up.tail = (0.90 * sx, -0.20, 2.10)
        b_arm_up.parent = b_spine2

        b_arm_fore = eb.new(f"arm_{lado}_forearm")
        b_arm_fore.head = (0.90 * sx, -0.20, 2.10)
        b_arm_fore.tail = (1.10 * sx, -0.40, 1.45)
        b_arm_fore.parent = b_arm_up

        b_hand = eb.new(f"hand_{lado}")
        b_hand.head = (1.10 * sx, -0.40, 1.45)
        b_hand.tail = (1.20 * sx, -0.60, 1.05)
        b_hand.parent = b_arm_fore

        # 9. Brazos Secundarios Pectorales (Canalizadores celestiales)
        b_arm_sub_up = eb.new(f"arm_sub_{lado}_upper")
        b_arm_sub_up.head = (0.28 * sx, -0.22, 2.25)
        b_arm_sub_up.tail = (0.50 * sx, -0.38, 1.85)
        b_arm_sub_up.parent = b_spine1

        b_arm_sub_fore = eb.new(f"arm_sub_{lado}_forearm")
        b_arm_sub_fore.head = (0.50 * sx, -0.38, 1.85)
        b_arm_sub_fore.tail = (0.58 * sx, -0.52, 1.45)
        b_arm_sub_fore.parent = b_arm_sub_up

        # 10. Piernas Rapaces Digitígradas (Levitantes)
        b_leg_thigh = eb.new(f"leg_{lado}_thigh")
        b_leg_thigh.head = (0.28 * sx, 0.0, 1.45)
        b_leg_thigh.tail = (0.35 * sx, 0.15, 0.85)
        b_leg_thigh.parent = b_pelvis

        b_leg_shin = eb.new(f"leg_{lado}_shin")
        b_leg_shin.head = (0.35 * sx, 0.15, 0.85)
        b_leg_shin.tail = (0.32 * sx, -0.15, 0.35)
        b_leg_shin.parent = b_leg_thigh

        b_foot = eb.new(f"foot_{lado}")
        b_foot.head = (0.32 * sx, -0.15, 0.35)
        b_foot.tail = (0.30 * sx, -0.35, 0.05)
        b_foot.parent = b_leg_shin

    bpy.ops.object.mode_set(mode='OBJECT')
    return arm_obj

def build_boss_mesh(mats):
    """Construye la geometría anatómica detallada de Azra'Koth asociada a huesos."""
    b = dl.MB("SK_Boss_AngelCthulhu")
    DC, AB, AG, SG, EC, EW = (
        mats["M_Bio_DarkChitin"], mats["M_Angel_Bone"], mats["M_Angel_Gold"],
        mats["M_Bio_AcidGreen"], mats["M_Bio_EyeCrimson"], mats["M_Angel_EnergyWing"]
    )

    # -------------------------------------------------------------------------
    # 1. ROOT & PELVIS
    # -------------------------------------------------------------------------
    b.bone("root")
    # Glifo sagrado circular de levitación en el suelo
    b.cyl(0.85, 0.04, (0, 0, 0.02), seg=24, m=SG)
    b.cyl(0.70, 0.06, (0, 0, 0.03), seg=20, m=AG)

    b.bone("pelvis")
    # Cadera blindada angulada de quitina
    b.box((0.75, 0.55, 0.40), (0, 0, 1.50), m=DC)
    b.box((0.60, 0.45, 0.30), (0, -0.12, 1.48), m=AB)
    # Espolón pélvico inferior
    b.cyl(0.12, 0.35, (0, 0.08, 1.25), rot=(0.3, 0, 0), seg=12, m=AG)

    # -------------------------------------------------------------------------
    # 2. COLUMNA VERTEBRAL Y TORSO ACORAZADO
    # -------------------------------------------------------------------------
    b.bone("spine_01")
    # Parte baja del torso y costillas óseas
    b.box((0.70, 0.50, 0.55), (0, -0.04, 1.95), m=DC)
    for c_i in range(3):
        cz = 1.75 + c_i * 0.15
        b.cyl(0.04, 0.65, (0, -0.18, cz), rot=(0, math.pi/2, 0), seg=12, m=AB)

    b.bone("spine_02")
    # Torso superior acorazado con corazón bio-celestial expuesto
    b.box((0.85, 0.60, 0.65), (0, -0.08, 2.50), m=DC)
    # Placas pectorales estilizadas serafín
    b.box((0.36, 0.12, 0.42), (-0.22, -0.34, 2.55), rot=(0.15, -0.15, 0), m=AB)
    b.box((0.36, 0.12, 0.42), (0.22, -0.34, 2.55), rot=(0.15, 0.15, 0), m=AB)
    # Núcleo / Corazón de Savia Primordial esmeralda
    b.sph(0.18, (0, -0.32, 2.45), u=16, v=10, m=SG)
    # Aros dorados de contención alrededor del corazón
    b.cyl(0.22, 0.04, (0, -0.30, 2.45), rot=(math.pi/2, 0, 0), seg=18, m=AG)

    # Espina dorsal exterior con púas óseas
    for s_i in range(5):
        sz = 2.20 + s_i * 0.14
        b.cyl(0.05, 0.35, (0, 0.28, sz), rot=(-0.4, 0, 0), seg=10, m=AB)

    # -------------------------------------------------------------------------
    # 3. CUELLO Y CABEZA CEFALÓPODA ELDRITCH
    # -------------------------------------------------------------------------
    b.bone("neck")
    b.cyl(0.22, 0.40, (0, -0.12, 2.95), rot=(0.12, 0, 0), seg=16, m=DC)

    b.bone("head")
    # Domo craneal abovedado alargado hacia atrás (Cthulhu Bio)
    b.sph(0.42, (0, -0.18, 3.42), scale=(0.85, 1.35, 1.05), u=20, v=12, m=DC)
    # Cresta sagrada frontal en oro serafín
    b.box((0.08, 0.55, 0.25), (0, -0.35, 3.55), rot=(0.35, 0, 0), m=AG)

    # 8 Ojos estigmáticos carmesí laterales (4 a cada lado)
    for eye_i in range(4):
        ey = -0.32 + eye_i * 0.08
        ez = 3.32 + eye_i * 0.06
        b.sph(0.05, (-0.32, ey, ez), u=10, v=6, m=EC)
        b.sph(0.05, (0.32, ey, ez), u=10, v=6, m=EC)

    # Fauce central de triple mandíbula radial
    b.cyl(0.16, 0.15, (0, -0.42, 3.10), rot=(0.5, 0, 0), seg=12, m=DC)
    b.sph(0.08, (0, -0.44, 3.10), u=8, v=6, m=SG)

    # -------------------------------------------------------------------------
    # 4. AUREOLA SERAFÍN FLOTANTE
    # -------------------------------------------------------------------------
    b.bone("halo_root")
    # Anillo principal de luz dorada/verde
    n_halo = 16
    r_halo = 0.55
    for h_i in range(n_halo):
        h_ang = h_i * (2.0 * math.pi / n_halo)
        hx = r_halo * math.cos(h_ang)
        hy = -0.15 + r_halo * math.sin(h_ang) * 0.75
        b.cyl(0.03, 0.12, (hx, hy, 4.05), rot=(0, math.pi/2, -h_ang), seg=8, m=AG)
        # 8 Espinas radiales salientes
        if h_i % 2 == 0:
            b.cyl(0.02, 0.22, (hx * 1.15, hy, 4.05), rot=(0, math.pi/2, -h_ang), seg=6, m=AB)

    # -------------------------------------------------------------------------
    # 5. 4 EXTREMIDADES MANDIBULARES ARTICULADAS (EN VEZ DE TENTÁCULOS)
    # -------------------------------------------------------------------------
    pos_queliceros_mesh = [
        ("mandible_l1", -0.22, -0.35, 3.15, -0.2),
        ("mandible_l2", -0.12, -0.42, 2.95, -0.1),
        ("mandible_r1",  0.22, -0.35, 3.15,  0.2),
        ("mandible_r2",  0.12, -0.42, 2.95,  0.1),
    ]
    for b_nom, qx, qy, qz, rot_y in pos_queliceros_mesh:
        # Base de la extremidad articulada
        b.bone(f"{b_nom}_base")
        b.box((0.08, 0.12, 0.25), (qx * 0.8, qy * 0.85, qz - 0.10), rot=(0.2, rot_y, 0), m=DC)
        b.cyl(0.04, 0.10, (qx * 0.8, qy * 0.85, qz - 0.10), seg=8, m=AG)

        # Falange intermedia con espinas laterales
        b.bone(f"{b_nom}_mid")
        b.box((0.07, 0.10, 0.32), (qx * 1.05, qy - 0.12, qz - 0.32), rot=(0.4, rot_y * 1.2, 0), m=AB)
        b.cyl(0.02, 0.14, (qx * 1.20, qy - 0.12, qz - 0.32), rot=(0, 0, 0.5), seg=6, m=DC)

        # Quelícero / Garra afilada terminal
        b.bone(f"{b_nom}_claw")
        b.cyl(0.035, 0.30, (qx * 1.0, qy - 0.32, qz - 0.55), rot=(0.6, rot_y * 0.8, 0), seg=8, m=AG)
        b.sph(0.04, (qx * 0.9, qy - 0.45, qz - 0.68), scale=(0.5, 0.5, 1.8), u=6, v=4, m=SG)

    # -------------------------------------------------------------------------
    # 6. 6 ALAS SERAFÍN BIOMECÁNICAS
    # -------------------------------------------------------------------------
    for lado, sx in [("l", -1.0), ("r", 1.0)]:
        # --- Alas Superiores (Colosales) ---
        b.bone(f"wing_{lado}_upper_01")
        # Brazo estructural óseo
        b.cyl(0.09, 1.40, (0.70 * sx, 0.28, 3.15), rot=(0.3, 0.7 * sx, 0), seg=12, m=DC)
        b.box((0.14, 0.18, 0.25), (0.45 * sx, 0.22, 2.90), m=AG)

        b.bone(f"wing_{lado}_upper_02")
        b.cyl(0.07, 1.60, (1.80 * sx, 0.50, 3.95), rot=(0.2, 0.5 * sx, 0), seg=10, m=AB)
        # Plumas serafín de energía verde translúcida / estigmática
        for p_i in range(6):
            px = (1.40 + p_i * 0.22) * sx
            py = 0.45 + p_i * 0.05
            pz = 3.65 + p_i * 0.12
            b.box((0.12, 0.02, 0.65), (px, py, pz - 0.25), rot=(-0.2, 0.3 * sx, 0.1 * sx), m=EW)

        # --- Alas Medias (Acorazadas) ---
        b.bone(f"wing_{lado}_mid_01")
        b.cyl(0.08, 1.20, (0.75 * sx, 0.24, 2.50), rot=(0.1, 0.9 * sx, 0), seg=10, m=DC)

        b.bone(f"wing_{lado}_mid_02")
        b.cyl(0.06, 1.10, (1.70 * sx, 0.42, 2.72), rot=(0.1, 0.8 * sx, 0), seg=8, m=AB)
        # Placas defensivas superpuestas
        for d_i in range(4):
            dx = (1.20 + d_i * 0.22) * sx
            b.box((0.16, 0.04, 0.45), (dx, 0.38, 2.65 - d_i * 0.06), rot=(0, 0.4 * sx, 0), m=DC)

        # --- Alas Inferiores (Estabilizadoras) ---
        b.bone(f"wing_{lado}_low_01")
        b.cyl(0.07, 0.95, (0.60 * sx, 0.18, 1.65), rot=(-0.2, 1.1 * sx, 0), seg=8, m=DC)

        b.bone(f"wing_{lado}_low_02")
        b.cyl(0.05, 0.90, (1.35 * sx, 0.30, 1.20), rot=(-0.3, 1.0 * sx, 0), seg=8, m=AG)
        b.box((0.12, 0.02, 0.50), (1.40 * sx, 0.30, 1.05), rot=(-0.3, 1.0 * sx, 0), m=EW)

        # -------------------------------------------------------------------------
        # 7. BRAZOS PRIMARIOS Y GARRAS
        # -------------------------------------------------------------------------
        b.bone(f"arm_{lado}_upper")
        # Hombro acorazado con hombrera serafín
        b.sph(0.18, (0.55 * sx, -0.10, 2.65), scale=(1.2, 1.0, 1.3), u=12, v=8, m=AG)
        b.cyl(0.10, 0.70, (0.70 * sx, -0.15, 2.35), rot=(0.3, 0.4 * sx, 0), seg=12, m=DC)

        b.bone(f"arm_{lado}_forearm")
        b.cyl(0.08, 0.85, (1.00 * sx, -0.30, 1.75), rot=(0.4, 0.3 * sx, 0), seg=10, m=AB)
        # Espolón dorsal del codo
        b.cyl(0.03, 0.28, (0.95 * sx, -0.15, 2.10), rot=(-0.6, 0, 0), seg=8, m=DC)

        b.bone(f"hand_{lado}")
        # Muñeca y palma
        b.box((0.16, 0.18, 0.16), (1.15 * sx, -0.50, 1.25), m=DC)
        # 4 Garras largas hipertrofiadas
        for f_i in range(4):
            fx = (1.10 + f_i * 0.04) * sx
            fy = -0.55 - f_i * 0.06
            fz = 1.15 - f_i * 0.08
            b.cyl(0.025, 0.32, (fx, fy, fz), rot=(0.6, 0.2 * sx, 0), seg=6, m=AG)

        # -------------------------------------------------------------------------
        # 8. BRAZOS SECUNDARIOS PECTORALES
        # -------------------------------------------------------------------------
        b.bone(f"arm_sub_{lado}_upper")
        b.cyl(0.06, 0.48, (0.38 * sx, -0.30, 2.05), rot=(0.4, 0.3 * sx, 0), seg=8, m=DC)

        b.bone(f"arm_sub_{lado}_forearm")
        b.cyl(0.05, 0.50, (0.54 * sx, -0.45, 1.65), rot=(0.5, 0.2 * sx, 0), seg=8, m=AB)
        # Garra canalizadora
        b.sph(0.06, (0.58 * sx, -0.52, 1.45), u=8, v=6, m=SG)

        # -------------------------------------------------------------------------
        # 9. PIERNAS RAPACES DIGITÍGRADAS
        # -------------------------------------------------------------------------
        b.bone(f"leg_{lado}_thigh")
        b.cyl(0.12, 0.70, (0.32 * sx, 0.08, 1.15), rot=(-0.2, 0.1 * sx, 0), seg=12, m=DC)
        b.box((0.18, 0.22, 0.25), (0.32 * sx, -0.02, 1.30), m=AB)

        b.bone(f"leg_{lado}_shin")
        b.cyl(0.09, 0.75, (0.34 * sx, 0.0, 0.60), rot=(0.4, 0, 0), seg=10, m=DC)
        # Espolón tibial posterior
        b.cyl(0.03, 0.25, (0.34 * sx, 0.18, 0.75), rot=(-0.7, 0, 0), seg=6, m=AG)

        b.bone(f"foot_{lado}")
        # Tarso y garras rapaces
        b.box((0.14, 0.22, 0.12), (0.31 * sx, -0.22, 0.20), m=DC)
        # 3 Garras frontales y 1 trasera
        for g_i in range(3):
            gx = (0.26 + g_i * 0.05) * sx
            b.cyl(0.025, 0.25, (gx, -0.35, 0.12), rot=(0.7, 0, 0), seg=6, m=AG)
        b.cyl(0.025, 0.20, (0.31 * sx, -0.08, 0.16), rot=(-0.7, 0, 0), seg=6, m=AG)

    return b.build(COL_BOSS)

def renderizar_cuatro_vistas(mesh_obj, arm_obj):
    """Genera render de 4 vistas (Frontal, Trasera, Acción/Ataque y FPS) según Reglas 4 y 5."""
    sc = bpy.context.scene
    motores = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
    if 'CYCLES' in motores:
        sc.render.engine = 'CYCLES'
        sc.cycles.samples = 64
        sc.cycles.use_denoising = True
    elif 'BLENDER_EEVEE_NEXT' in motores:
        sc.render.engine = 'BLENDER_EEVEE_NEXT'
    else:
        sc.render.engine = 'BLENDER_EEVEE'

    sc.render.resolution_x = 1024
    sc.render.resolution_y = 1024
    sc.render.film_transparent = False

    w = bpy.data.worlds.get("DarxBossWorldAngel") or bpy.data.worlds.new("DarxBossWorldAngel")
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = (0.015, 0.018, 0.022, 1.0)
    w.node_tree.nodes["Background"].inputs[1].default_value = 1.0
    sc.world = w

    # Objetos a encuadrar
    objs = [mesh_obj, arm_obj]
    center_focus = (0, -0.15, 2.50)

    # 1. Vista Frontal
    out_front = os.path.join(ARTIFACTS_DIR, "preview_boss_angel_cthulhu_frontal.png")
    dl.snap(objs, out_front, focus=center_focus, dist=7.8, yaw=0.0, pitch=8.0, res=1024)

    # 2. Vista Trasera (Apreciación del hexapulso alar y aureola)
    out_back = os.path.join(ARTIFACTS_DIR, "preview_boss_angel_cthulhu_trasera.png")
    dl.snap(objs, out_back, focus=center_focus, dist=7.8, yaw=180.0, pitch=8.0, res=1024)

    # 3. Vista de Acción / Ataque (Perspectiva dinámica 3/4)
    out_action = os.path.join(ARTIFACTS_DIR, "preview_boss_angel_cthulhu_ataque.png")
    dl.snap(objs, out_action, focus=center_focus, dist=7.5, yaw=35.0, pitch=15.0, res=1024)

    # 4. Vista Primera Persona (FPS: Desde la perspectiva del jugador a 180cm de altura)
    out_fps = os.path.join(ARTIFACTS_DIR, "preview_boss_angel_cthulhu_fps.png")
    dl.snap(objs, out_fps, focus=(0, -0.20, 2.20), dist=4.5, yaw=0.0, pitch=-5.0, res=1024)

    print("DarX | Renders de 4 vistas generados con éxito:")
    print(f"  - Frontal: {out_front}")
    print(f"  - Trasera: {out_back}")
    print(f"  - Ataque: {out_action}")
    print(f"  - FPS: {out_fps}")

    return [out_front, out_back, out_action, out_fps]

def main():
    print("=" * 80)
    print("DarX | Generando Jefe: Azra'Koth, El Serafín Primordial (Ángel-Cthulhu)...")
    print("=" * 80)

    dl.wipe(COL_BOSS)
    dl.coll(COL_BOSS)
    mats = crear_materiales_boss()

    print("DarX | Construyendo armadura y jerarquía de huesos...")
    arm_obj = build_boss_armature()

    print("DarX | Modelando anatomía híbrida (cabeza cefalópoda, quelíceros, 6 alas, aureola)...")
    mesh_obj = build_boss_mesh(mats)

    print("DarX | Vinculando malla a la armadura con pesos directos...")
    dl.bind(mesh_obj, arm_obj)

    print("DarX | Generando previsualizaciones de 4 vistas canónicas...")
    renders = renderizar_cuatro_vistas(mesh_obj, arm_obj)

    print("DarX | Exportando FBX canónico (-Y -> +X)...")
    os.makedirs(FBX_DIR, exist_ok=True)
    mesh_obj.location = (0, 0, 0)
    arm_obj.location = (0, 0, 0)
    bpy.context.view_layer.update()

    # Seleccionar ambos objetos para exportar como SkeletalMesh canónico
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    arm_obj.select_set(True)
    bpy.context.view_layer.objects.active = arm_obj

    fbx_out = os.path.join(FBX_DIR, "SK_Boss_AngelCthulhu.fbx")
    bpy.ops.export_scene.fbx(
        filepath=fbx_out,
        use_selection=True,
        axis_forward='-Y',
        axis_up='Z',
        apply_scale_options='FBX_SCALE_ALL',
        object_types={'ARMATURE', 'MESH'},
        use_mesh_modifiers=True,
        mesh_smooth_type='FACE',
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        armature_nodetype='NULL'
    )
    print(f"DarX | FBX exportado con éxito en: {fbx_out}")
    print("=" * 80)

if __name__ == "__main__":
    main()
