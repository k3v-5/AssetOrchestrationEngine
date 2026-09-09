import unittest
import os
import json
import tempfile
import subprocess

class TestV1_1Features(unittest.TestCase):
    def test_cli_parsing_lod_and_qa(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.json")
            output_dir = os.path.join(tmpdir, "out")

            batch_config = {
                "batch_id": "cli_v1_1_test",
                "recipes": [
                    {
                        "recipe_id": "Ninja",
                        "base_mesh": "ninja.fbx",
                        "appearance_id": "ninja_app",
                        "lod_config": {
                            "levels": [50, 25],
                            "keep_inverted_hull": [True, False]
                        },
                        "qa_limits": {
                            "max_triangles": 10000,
                            "max_bones": 50,
                            "max_texture_res": 2048
                        }
                    }
                ]
            }

            with open(input_file, 'w') as f:
                json.dump(batch_config, f)

            # Run CLI script
            cmd = ["python", "-m", "aoe_cli", "build_batch", "--input", input_file, "--output", output_dir]
            result = subprocess.run(cmd, capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, f"CLI Failed: {result.stderr}")
            self.assertIn("Pipeline Execution Complete!", result.stdout)

if __name__ == '__main__':
    unittest.main()
