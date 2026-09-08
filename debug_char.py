import json
import dataclasses
from src.aoe_ir.appearance import AppearanceProfile, AppearanceFamily, StyleProfile, ShadingProfile, ShaderModel, OutlineProfile, OutlineMethod, StyleProfileType
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner
from tests.fixtures.humanoid_fixture import create_humanoid_fixture

def _dataclass_to_dict(obj):
    if dataclasses.is_dataclass(obj):
        return {k: _dataclass_to_dict(v) for k, v in dataclasses.asdict(obj).items()}
    elif isinstance(obj, list):
        return [_dataclass_to_dict(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: _dataclass_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, 'value'): # Handle Enums
        return obj.value
    else:
        return obj

pbr_app = AppearanceProfile(
    appearance_id="pbr_base",
    family=AppearanceFamily.PBR,
    style=StyleProfile(shading=ShadingProfile(model=ShaderModel.PBR))
)

char_ir = create_humanoid_fixture(pbr_app)
char_ir.metadata["active_pose"] = "REST"

runner = BlenderHeadlessRunner()
args = {
    "asset": _dataclass_to_dict(char_ir),
    "filepath": "debug_char.blend"
}

res = runner.run_script("tests/integration/blender/executor.py", args)
print(json.dumps(res, indent=2))
