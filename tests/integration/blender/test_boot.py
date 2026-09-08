import unittest
import os
import tempfile
from src.aoe_ir.backends.headless_runner import BlenderHeadlessRunner

class TestBlenderBoot(unittest.TestCase):
    def setUp(self):
        self.runner = BlenderHeadlessRunner()

        # Skip if Blender is not installed
        if not self.runner.check_availability():
            self.skipTest("Blender runtime unavailable")

    def test_blender_headless_boot(self):
        # Create a dummy python script for Blender
        script_content = """
import bpy
import json
import os

def main():
    args_str = os.environ.get("AOE_BLENDER_ARGS", "{}")
    args = json.loads(args_str)

    # Save a dummy blend file to prove it works
    filepath = args.get("filepath", "dummy.blend")
    bpy.ops.wm.save_as_mainfile(filepath=filepath)

    result = {
        "status": "SUCCESS",
        "objects_count": len(bpy.data.objects),
        "filepath": filepath
    }
    print(f"AOE_RESULT:{json.dumps(result)}")

if __name__ == "__main__":
    main()
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = os.path.join(tmpdir, "test_boot.py")
            blend_path = os.path.join(tmpdir, "out.blend")

            with open(script_path, "w") as f:
                f.write(script_content)

            # Run the script
            res = self.runner.run_script(script_path, args={"filepath": blend_path})

            self.assertEqual(res["status"], "SUCCESS")
            self.assertTrue(os.path.exists(blend_path))

if __name__ == "__main__":
    unittest.main()
