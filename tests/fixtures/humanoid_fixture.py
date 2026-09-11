from src.aoe_ir.character import CharacterIR, CharacterMeshIR, SemanticRegionTag, CharacterSemanticRegionIR
from src.aoe_ir.skeleton import SkeletonIR, BoneIR, SkinningIR, VertexWeightIR
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, StyleProfileType
from src.aoe_ir.pose import PoseIR, PoseTransformIR
from src.aoe_ir.animation import AnimationFoundationIR, AnimationClipIR
import math

def create_humanoid_fixture(appearance: AppearanceProfile) -> CharacterIR:
    """Creates a basic programmatic humanoid fixture (IR only)."""

    # Minimal Humanoid Skeleton
    # root -> pelvis -> spine -> neck -> head
    #                -> clavicle_L -> upper_arm_L -> forearm_L -> hand_L
    #                -> clavicle_R -> upper_arm_R -> forearm_R -> hand_R
    #        -> thigh_L -> shin_L -> foot_L
    #        -> thigh_R -> shin_R -> foot_R
    bones = {
        "root": BoneIR("root", head=(0,0,0), tail=(0,0,0.1), children=["pelvis"]),
        "pelvis": BoneIR("pelvis", parent="root", head=(0,0,1.0), tail=(0,0,1.1), children=["spine", "thigh_L", "thigh_R"]),
        "spine": BoneIR("spine", parent="pelvis", head=(0,0,1.1), tail=(0,0,1.4), children=["neck", "clavicle_L", "clavicle_R"]),
        "neck": BoneIR("neck", parent="spine", head=(0,0,1.4), tail=(0,0,1.5), children=["head"]),
        "head": BoneIR("head", parent="neck", head=(0,0,1.5), tail=(0,0,1.7)),

        "clavicle_L": BoneIR("clavicle_L", parent="spine", head=(0,0,1.4), tail=(0.2,0,1.4), children=["upper_arm_L"]),
        "upper_arm_L": BoneIR("upper_arm_L", parent="clavicle_L", head=(0.2,0,1.4), tail=(0.5,0,1.4), children=["forearm_L"]),
        "forearm_L": BoneIR("forearm_L", parent="upper_arm_L", head=(0.5,0,1.4), tail=(0.8,0,1.4), children=["hand_L"]),
        "hand_L": BoneIR("hand_L", parent="forearm_L", head=(0.8,0,1.4), tail=(1.0,0,1.4)),

        "clavicle_R": BoneIR("clavicle_R", parent="spine", head=(0,0,1.4), tail=(-0.2,0,1.4), children=["upper_arm_R"]),
        "upper_arm_R": BoneIR("upper_arm_R", parent="clavicle_R", head=(-0.2,0,1.4), tail=(-0.5,0,1.4), children=["forearm_R"]),
        "forearm_R": BoneIR("forearm_R", parent="upper_arm_R", head=(-0.5,0,1.4), tail=(-0.8,0,1.4), children=["hand_R"]),
        "hand_R": BoneIR("hand_R", parent="forearm_R", head=(-0.8,0,1.4), tail=(-1.0,0,1.4)),

        "thigh_L": BoneIR("thigh_L", parent="pelvis", head=(0.1,0,1.0), tail=(0.1,0,0.5), children=["shin_L"]),
        "shin_L": BoneIR("shin_L", parent="thigh_L", head=(0.1,0,0.5), tail=(0.1,0,0.1), children=["foot_L"]),
        "foot_L": BoneIR("foot_L", parent="shin_L", head=(0.1,0,0.1), tail=(0.1,0.2,0.0)),

        "thigh_R": BoneIR("thigh_R", parent="pelvis", head=(-0.1,0,1.0), tail=(-0.1,0,0.5), children=["shin_R"]),
        "shin_R": BoneIR("shin_R", parent="thigh_R", head=(-0.1,0,0.5), tail=(-0.1,0,0.1), children=["foot_R"]),
        "foot_R": BoneIR("foot_R", parent="shin_R", head=(-0.1,0,0.1), tail=(-0.1,0.2,0.0))
    }

    skeleton = SkeletonIR(skeleton_id="humanoid_skeleton", bones=bones, root_bone="root")

    # We will procedurally generate meshes in blender based on bones, but we assign semantics here
    semantic_regions = [
        CharacterSemanticRegionIR(region_id=SemanticRegionTag.HEAD, mesh_id="body_mesh", vertex_indices=[]),
        CharacterSemanticRegionIR(region_id=SemanticRegionTag.FACE, mesh_id="body_mesh", vertex_indices=[]),
        CharacterSemanticRegionIR(region_id=SemanticRegionTag.HAIR, mesh_id="hair_mesh", vertex_indices=[]),
        CharacterSemanticRegionIR(region_id=SemanticRegionTag.EYES, mesh_id="body_mesh", vertex_indices=[]),
        CharacterSemanticRegionIR(region_id=SemanticRegionTag.BODY, mesh_id="body_mesh", vertex_indices=[])
    ]

    # Poses
    rest_pose = PoseIR(pose_id="REST", bone_transforms={})
    pose_a = PoseIR(pose_id="POSE_A", bone_transforms={
        "upper_arm_L": PoseTransformIR(rotation_euler=(0, 0, math.radians(45))) # Arm raised
    })
    pose_b = PoseIR(pose_id="POSE_B", bone_transforms={
        "upper_arm_R": PoseTransformIR(rotation_euler=(0, 0, math.radians(-45)))
    })
    pose_c = PoseIR(pose_id="POSE_C", bone_transforms={
        "upper_arm_L": PoseTransformIR(rotation_euler=(0, 0, math.radians(90))),
        "upper_arm_R": PoseTransformIR(rotation_euler=(0, 0, math.radians(-90))),
        "spine": PoseTransformIR(rotation_euler=(math.radians(20), 0, 0)) # leaning forward
    })

    animation = AnimationFoundationIR(
        rest_pose=rest_pose,
        clips={
            "pose_a": AnimationClipIR("pose_a", 1, keyframes={0: pose_a}),
            "pose_b": AnimationClipIR("pose_b", 1, keyframes={0: pose_b}),
            "pose_c": AnimationClipIR("pose_c", 1, keyframes={0: pose_c}),
        }
    )

    return CharacterIR(
        character_id="humanoid_test",
        meshes={
            "body_mesh": CharacterMeshIR("body_mesh"),
            "hair_mesh": CharacterMeshIR("hair_mesh")
        },
        skeleton=skeleton,
        skinning={"body_mesh": SkinningIR("body_skin")},
        semantic_regions=semantic_regions,
        appearance=appearance,
        animation=animation
    )
