with open("src/aoe_ir/animation.py", "r") as f:
    code = f.read()

new_struct = """@dataclass
class AnimationLayerIR:
    layer_id: str
    clip_id: str
    weight: float = 1.0
    blend_mode: str = "ADDITIVE" # or OVERRIDE

@dataclass
class AnimationGraphIR:
    graph_id: str
    base_clip_id: str
    layers: List[AnimationLayerIR] = field(default_factory=list)
"""

code = code + "\n" + new_struct
with open("src/aoe_ir/animation.py", "w") as f:
    f.write(code)
