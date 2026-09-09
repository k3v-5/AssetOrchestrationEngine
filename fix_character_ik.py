with open("src/aoe_ir/character.py", "r") as f:
    code = f.read()

import_str = "from .animation import AnimationFoundationIR"
new_import = "from .animation import AnimationFoundationIR\nfrom .ik import IKSolverConfigIR"
code = code.replace(import_str, new_import)

old_field = "    animation: Optional[AnimationFoundationIR] = None"
new_field = "    animation: Optional[AnimationFoundationIR] = None\n    ik_config: Optional[IKSolverConfigIR] = None"
code = code.replace(old_field, new_field)

with open("src/aoe_ir/character.py", "w") as f:
    f.write(code)
